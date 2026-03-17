from django.http import JsonResponse
from common.logger import logger
from functools import wraps
from typing import List, Callable, Any
from dotenv import dotenv_values
import json
import os


def validate_post_request_with_fields(expected_fields: List[str]) -> Callable:
    """
    Decorator to validate POST requests with expected fields in the body.

    Args:
        expected_fields (List[str]): The list of expected fields in the request body.

    Returns:
        Callable: The decorator function.
    """
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def _wrapped_view(request: Any, *args: Any, **kwargs: Any) -> JsonResponse:
            if request.method != 'POST':
                return JsonResponse({"status": 405, "message": "Method not allowed. Only POST requests are allowed."})

            body_params = request.body.decode('utf-8')
            if not body_params:
                return JsonResponse({"status": 400, "message": f"No parameters in body provided. Expected {expected_fields}"})

            body_params = json.loads(body_params)
            missing_fields = [
                field for field in expected_fields if field not in body_params]

            if missing_fields:
                return JsonResponse({"status": 400, "message": f"Missing fields in body: {missing_fields}"})

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


def validate_request_has_files() -> Callable:
    """
    Decorator to validate that the request has uploaded files.

    Returns:
        Callable: The decorator function.
    """
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def _wrapped_view(request: Any, *args: Any, **kwargs: Any) -> JsonResponse:
            if not request.FILES:
                return JsonResponse({"status": 400, "message": "No files uploaded"})

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


def user_with_id_exists(user_id: str) -> bool:
    """
    Check if a user with a specific ID exists.

    Args:
        user_id (str): The ID of the user.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    from apps.users.models import User
    return User.objects.filter(id=user_id).exists()


def validate_environment():
    """
    Validate that all required environment variables and files are set.

    Raises:
        EnvironmentError: If any of the required environment variables or files are missing.
    """
    from config.paths import TMP_DIR, STORAGE_DIR, CHROMA_SQLITE_DB_DIR, CHROMA_SQLITE_PATH, DJANGO_SQLITE_DB_PATH

    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
        logger.debug(f"Created temporary directory at {TMP_DIR}")

    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
        logger.debug(f"Created storage directory at {STORAGE_DIR}")

    if not os.path.exists(CHROMA_SQLITE_DB_DIR):
        os.makedirs(CHROMA_SQLITE_DB_DIR)
        logger.debug(f"Created ChromaDB directory at {CHROMA_SQLITE_DB_DIR}")

    if not os.path.exists(CHROMA_SQLITE_PATH):
        raise FileNotFoundError(
            f"ChromaDB database not found at {CHROMA_SQLITE_PATH}. Please get the database file and retry.")

    if not os.path.exists(DJANGO_SQLITE_DB_PATH):
        raise FileNotFoundError(
            f"Django database not found at {DJANGO_SQLITE_DB_PATH}. Please get the database file and retry.")

    if not os.path.exists('.env'):
        raise EnvironmentError("Missing .env file")

    required_vars = [
        'DJANGO_SECRET_KEY',
        'JWT_SECRET_KEY',
        'GOOGLE_APPLICATION_CREDENTIALS',
        'YOU_API_KEY_RAG',
        'YOU_API_KEY_SEARCH'
    ]

    env = dotenv_values('.env')

    missing_vars = []
    for var in required_vars:
        if var not in env:
            missing_vars.append(var)

        elif var.strip() == '':
            missing_vars.append(var)

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variable(s): {', '.join(missing_vars)}")

    if not os.path.exists(env['GOOGLE_APPLICATION_CREDENTIALS']):
        raise EnvironmentError(
            "Google application credentials file does not exist.")

    logger.debug("Environment is configured correctly.")
