# core/middleware.py

from django.middleware.csrf import CsrfViewMiddleware
from django.http import JsonResponse
from django.conf import settings
from django.urls import resolve

class CsrfExemptMiddleware(CsrfViewMiddleware):
    # List of paths to be exempt from CSRF
    exempt_paths = [
        '/auth/registration/',  # Add any other URLs here that need to be exempt
    ]

    def process_request(self, request):
        # Check if the request path is in the exempt paths list
        for path in self.exempt_paths:
            if request.path.startswith(path):
                self._disable_csrf(request)
                break
        super().process_request(request)

    def process_exception(self, request, exception):
        # Handle CSRF exception (if any)
        if isinstance(exception, CsrfViewMiddleware):
            return JsonResponse({'detail': 'CSRF token missing or incorrect.'}, status=403)
        return super().process_exception(request, exception)

    def _disable_csrf(self, request):
        """Disables CSRF checks for the current request."""
        request.csrf_processing_done = True
