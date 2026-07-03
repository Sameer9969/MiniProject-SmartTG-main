from django.shortcuts import redirect
from django.urls import reverse

class ConfirmLogoutMiddleware:
    """
    Middleware that ensures users see a confirmation page
    before logging out directly via /logout/ URL.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only trigger if user tries to access the logout URL directly
        try:
            logout_url = reverse('logout')  # e.g. /accounts/logout/
            confirm_url = reverse('confirm_logout')  # e.g. /accounts/logout/confirm/
        except Exception:
            return self.get_response(request)

        if request.path == logout_url and request.method == 'GET':
            # Redirect to confirmation page
            return redirect('confirm_logout')

        return self.get_response(request)


class LoginRequiredMiddleware:
    """
    Middleware that restricts access to certain pages
    for unauthenticated users.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that should be protected
        protected_paths = [
            reverse('wishlist'),
        ]

        # If user tries to access protected page without login
        if not request.user.is_authenticated and request.path in protected_paths:
            return redirect('login')

        return self.get_response(request)
