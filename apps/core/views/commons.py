# Standard Libraries
import json

# Third-party Libraries
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils import timezone

# Own Libraries
from config.enviroment_vars import settings


def javascript(request: HttpRequest):
    now = timezone.now()
    context = {
        "datetime": now.strftime("%d-%m-%YT%H:%M:%S%z"),
        "graphql_url": settings.GRAPHQL_URL,
        "site_name": settings.SITE_NAME,
        "select2_all": "",
    }
    urls = {
        "home": reverse("home"),
        "professionalSearch": reverse("core:professional:search"),
        "professionalRetrieve": reverse(
            "core:professional:retrieve", kwargs={"pk": "::"}
        ),
        "uploadAttachment": reverse("core:profesional_api_rest:user-attachments"),
    }

    context["urls"] = urls

    var = "let Django = " + json.dumps(context, indent=2)
    return HttpResponse(var, content_type="application/javascript")
