from django.contrib.auth import login_required


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return login_required(request)

        return self.get_response(request)