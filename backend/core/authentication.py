from rest_framework.authentication import SessionAuthentication
from django.conf import settings


class AppSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication that skips CSRF enforcement during local development (DEBUG=True)
    to eliminate cross-port localhost development friction across Vite dev ports (5173-5185).
    In production (DEBUG=False), full standard CSRF validation is strictly enforced.
    """

    def enforce_csrf(self, request):
        if getattr(settings, "DEBUG", False):
            return  # Skip CSRF check in local development mode
        return super().enforce_csrf(request)

