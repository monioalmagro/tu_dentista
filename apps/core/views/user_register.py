# Own Libraries
from apps.core.views.interfaces import PsychologyBaseView


class UserRegisterView(PsychologyBaseView):
    template_name = "core/user_register.html"
