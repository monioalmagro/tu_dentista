# Third-party Libraries
from django.urls import path, include

app_name = "core"

urlpatterns = [
    path("zona-usuario/", include("apps.core.urls.user"), name="user"),
    path("profesionales/", include("apps.core.urls.professional"), name="profesional"),
    path(
        "profesionales-apirest/",
        include("apps.core.urls.professional_api_rest"),
        name="profesional_api_rest",
    ),
]
