import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django')

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"User: {user} accessed {request.path} with method {request.method}")
