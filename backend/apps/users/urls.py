from django.urls import path
from apps.users.views import register, login, reset_chat_history, get_chat_history

urlpatterns = [
    path(
        route='register/',
        view=register,
        name='register'
    ),

    path(
        route='login/',
        view=login,
        name='login'
    ),

    path(
        route='reset_chat_history/',
        view=reset_chat_history,
        name='reset_chat_history'
    ),

    path(
        route='history/',
        view=get_chat_history,
        name='history'
    )
]
