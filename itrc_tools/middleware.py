# itrc_tools/middleware.py

from django.utils import timezone
from .models import SessionLog
from django.utils.deprecation import MiddlewareMixin

class SessionTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not request.session.get('session_start_time'):
                # Start a new session log
                session_log = SessionLog.objects.create(
                    user=request.user,
                    session_start=timezone.now()
                )
                request.session['session_log_id'] = session_log.id
                request.session['session_start_time'] = session_log.session_start.isoformat()

    def process_response(self, request, response):
        if request.user.is_authenticated:
            if 'session_log_id' in request.session:
                session_log_id = request.session['session_log_id']
                try:
                    session_log = SessionLog.objects.get(id=session_log_id, user=request.user)
                    if not session_log.session_end:
                        session_log.session_end = timezone.now()
                        session_log.save()
                        # Clear session data
                        del request.session['session_log_id']
                        del request.session['session_start_time']
                except SessionLog.DoesNotExist:
                    pass
        return response

# itrc_tools/middleware.py

import time
from .models import APIPerformanceLog
from django.utils.deprecation import MiddlewareMixin

class APIPerformanceMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request._start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, '_start_time'):
            duration = (time.time() - request._start_time) * 1000  # in milliseconds
            endpoint = request.path
            APIPerformanceLog.objects.create(
                endpoint=endpoint,
                response_time=duration,
                timestamp=timezone.now()
            )
        return response

# itrc_tools/middleware.py

from .models import ErrorLog
from django.utils.deprecation import MiddlewareMixin

class ErrorLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if hasattr(request, 'path'):
            path = request.path
        else:
            path = 'Unknown'
        
        error_type = '500'  # Default to server error
        message = str(exception)
        
        # Determine error type based on exception
        if isinstance(exception, Http404):
            error_type = '404'
        elif isinstance(exception, PermissionDenied):
            error_type = '403'
        elif isinstance(exception, BadRequest):
            error_type = '400'
        elif isinstance(exception, AuthenticationFailed):
            error_type = '401'
        # Add more specific exceptions as needed
        
        ErrorLog.objects.create(
            error_type=error_type,
            message=message,
            endpoint=path,
            timestamp=timezone.now()
        )
