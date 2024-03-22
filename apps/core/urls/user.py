# Third-party Libraries
from django.urls import path

# Own Libraries
from apps.core.views.user_register import UserRegisterView

app_name = "user"

urlpatterns = [
    path("registro/", UserRegisterView.as_view(), name="register"),
]
