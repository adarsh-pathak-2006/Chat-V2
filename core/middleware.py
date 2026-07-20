from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

@database_sync_to_async
def get_user(validated_token):
    try:
        user = User.objects.get(id=validated_token["user_id"])
        return user
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode("utf-8")
        parsed_query = parse_qs(query_string)
        
        token = parsed_query.get("token")
        
        if not token:
            scope["user"] = AnonymousUser()
            return await self.inner(scope, receive, send)

        try:
            # Validate token using SimpleJWT
            UntypedToken(token[0])
            # Decode token to get user id
            decoded_data = jwt_decode(token[0], settings.SECRET_KEY, algorithms=["HS256"])
            scope["user"] = await get_user(decoded_data)
        except (InvalidToken, TokenError, Exception) as e:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)

def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)
