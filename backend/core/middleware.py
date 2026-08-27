from django.http import HttpResponse

ALLOWED_ORIGIN_PREFIXES = (
    'http://localhost:',
    'http://127.0.0.1:',
    'https://frill-suitor-gone.ngrok-free.dev',
)


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get('Origin', '')
        allowed = any(origin.startswith(p) for p in ALLOWED_ORIGIN_PREFIXES)

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
