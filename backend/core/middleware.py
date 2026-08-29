from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import resolve, Resolver404

from .roles import can


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get('Origin', '')
        allowed = bool(origin) and (
            origin.startswith('http://localhost:')
            or origin.startswith('http://127.0.0.1:')
            or origin.endswith('.ngrok-free.app')
            or origin.endswith('.ngrok-free.dev')
        )

        if request.method == 'OPTIONS' and origin and allowed:
            response = HttpResponse()
        else:
            response = self.get_response(request)

        if allowed:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response


class RoleAccessMiddleware:
    """Restrict every /admin-panel/ route by the viewer's role.

    The role a user may use on a given admin-panel route is defined in
    core.roles.PERMISSIONS (keyed by URL name). Unauthenticated requests are
    left alone so the view's own @login_required can redirect to the login page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/admin-panel/'):
            return self.get_response(request)
        if not getattr(request.user, 'is_authenticated', False):
            return self.get_response(request)

        try:
            match = resolve(request.path_info)
        except Resolver404:
            return self.get_response(request)

        if not can(request.user, match.url_name):
            return render(request, 'core/403.html', status=403)

        return self.get_response(request)
