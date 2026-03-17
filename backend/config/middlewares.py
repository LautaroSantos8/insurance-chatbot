from common.logger import logger
from django.http import HttpRequest, JsonResponse
from dotenv import dotenv_values
import jwt


class RequestLoggerMiddleware:
    """Middleware to log incoming requests."""

    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response: The callable to get a response.
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        """
        Call method to handle the request.

        Args:
            request (HttpRequest): The incoming HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
        request_info = {
            'path': request.path,
            'method': request.method,
            'headers': dict(request.headers),
            'body': request.body.decode('utf-8'),
        }
        logger.debug(f"Received request ({request_info}) ")

        response = self.get_response(request)
        return response


class JWTAuthenticationMiddleware:
    """Middleware for JWT token authentication."""

    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response: The callable to get a response.
        """
        self.get_response = get_response
        self.allowed_paths = ['/users/login/', '/users/register/', '/admin/']

    def __call__(self, request: HttpRequest):
        """
        Call method to handle the request.

        Args:
            request (HttpRequest): The incoming HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
        for path in self.allowed_paths:
            if request.path.startswith(path):
                return self.get_response(request)

        if 'Authorization' not in request.headers:
            logger.warning(f'No auth header received.')
            return JsonResponse({'error': 'No Authorization header found'}, status=401)

        auth_header = request.headers['Authorization']
        if not auth_header.startswith('Bearer '):
            logger.warning(f'Invalid authentication header found.')
            return JsonResponse({'error': 'Invalid Authorization header'}, status=401)

        token = auth_header.split(' ')[1]

        decoded_token = jwt.decode(
            jwt=token,
            key=dotenv_values()['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )

        request.user_id = decoded_token['user_id']
        return self.get_response(request)
