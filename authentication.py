from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("auth_token")  # Read token from cookies
        if not token:
            return None  # No authentication if token is not in cookies

        return self.authenticate_credentials(token)
