# Standard Libraries
from typing import Any

# Own Libraries
from apps.core.views.interfaces import PsychologyBaseView


class ProfessionalRetrieveView(PsychologyBaseView):
    template_name = "core/professional_retrieve.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["original_id"] = kwargs["pk"]
        return context
