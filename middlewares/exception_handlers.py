import logging
from django.http import JsonResponse

logger = logging.getLogger('django')

class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            return JsonResponse({
                "success": False,
                "message": "Internal Server Error",
                "errors": str(e)
            }, status=500)
