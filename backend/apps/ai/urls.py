from apps.ai.views import ask_policy_assitant, quick_search, experimental_streaming_assistant
from django.urls import path


urlpatterns = [
    path(
        route='policy_insurance_assistant/',
        view=ask_policy_assitant,
        name='policy_insurance_assistant'
    ),

    path(
        route='experimental_streaming_assistant/',
        view=experimental_streaming_assistant,
        name='experimental_streaming_assistant'
    ),

    path(
        route='quick_search/',
        view=quick_search,
        name='quick_search'
    )
]
