# middleware.py
from django.shortcuts import redirect

class PreventAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/admin/') and not request.path.startswith('/login/') and not request.user.is_superuser:
            return redirect('login')  
        
        return self.get_response(request)


