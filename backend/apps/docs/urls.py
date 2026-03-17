from apps.docs.views import get_policy
from django.urls import path

# TODO: Future functionality: Upload your own documents
# path(
#    route='upload/',
#    view=upload_document,
#    name='upload'
# )

urlpatterns = [
    path(
        route="get_policy/",
        view=get_policy,
        name='get_policy'
    )
]
