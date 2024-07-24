from django.utils.deprecation import MiddlewareMixin
from .views import track_visit

class VisitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        track_visit(request)
        return None
