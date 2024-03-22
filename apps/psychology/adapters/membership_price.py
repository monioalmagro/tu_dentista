# Own Libraries
from apps.psychology.models import MembershipPrice
from utils.adapter import ModelAdapter


class MembershipPriceAdapter(ModelAdapter):
    model_class = MembershipPrice
