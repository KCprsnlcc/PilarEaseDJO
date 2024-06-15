# my_app/middleware.py

import pytz
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tz = pytz.timezone('Asia/Manila')
        request.current_time = datetime.now(tz)

    def process_response(self, request, response):
        if hasattr(request, 'current_time'):
            response['X-Current-Time'] = request.current_time.isoformat()
        return response
