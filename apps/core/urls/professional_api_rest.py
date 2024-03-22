# Third-party Libraries
from django.urls import path

# Own Libraries
from apps.core.api.user_attachment import RegisterUserAttachment

app_name = "profesional_api_rest"

urlpatterns = [
    path(
        "user-attachments/",
        RegisterUserAttachment.as_view(),
        name="user-attachments",
    ),
]
