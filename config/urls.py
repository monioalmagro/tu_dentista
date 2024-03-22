"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Third-party Libraries
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Own Libraries
from apps.core.views import javascript
from apps.core.views.interfaces import PsychologyBaseView

admin.site.site_title = "Psychology site admin"
admin.site.site_header = "Psychology administration"
admin.site.index_title = "Site administration"


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("javascript/", javascript, name="javascript"),
        path("", include("apps.core.urls", namespace="core")),
        path(
            "",
            PsychologyBaseView.as_view(
                template_name="home.html",
            ),
            name="home",
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
