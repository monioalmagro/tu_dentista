# Third-party Libraries
from django.urls import path

# Own Libraries
from apps.core.views.professional_retrieve import ProfessionalRetrieveView
from apps.core.views.professional_search import ProfessionalSearchView

app_name = "professional"

urlpatterns = [
    path(
        "buscador/",
        ProfessionalSearchView.as_view(),
        name="search",
    ),
    path(
        "detalle/<pk>/",
        ProfessionalRetrieveView.as_view(),
        name="retrieve",
    ),
]
