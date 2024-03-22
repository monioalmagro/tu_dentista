# Standard Libraries
import logging

# Third-party Libraries
import strawberry

# Own Libraries
from apps.psychology import psychology_constants
from apps.psychology.adapters.carreer import CarreerAdapter
from apps.psychology.adapters.city import CityAdapter
from apps.psychology.adapters.languages import LanguageAdapter
from apps.psychology.adapters.membership_price import MembershipPriceAdapter
from apps.psychology.adapters.specialization import SpecializationAdapter
from apps.psychology.adapters.user import UserAdapter
from apps.psychology.adapters.zone import ZoneAdapter
from apps.psychology.schema.inputs.user import (
    QueryListUserInput,
    QueryRetrieveUserInput,
)
from apps.psychology.schema.types.carreer import CarreerSelect2Type
from apps.psychology.schema.types.city import CitySelect2Type, ZoneSelect2Type
from apps.psychology.schema.types.membership_price import MembershipPriceType
from apps.psychology.schema.types.specialization import (
    SpecializationSelect2Type,
)
from apps.psychology.schema.types.user import ProfessionalType
from apps.psychology.schema.types.user_language import LanguageSelect2Type

logger = logging.getLogger(__name__)


@strawberry.type()
class Select2Queries:
    @strawberry.field()
    async def carreers(self) -> list[CarreerSelect2Type]:
        adapter = CarreerAdapter()
        adapter.user_id = None
        if results := await adapter.get_objects():
            return [
                CarreerSelect2Type.from_db_model(instance=carreer)
                for carreer in results
            ]
        return []

    @strawberry.field()
    async def cities(self) -> list[CitySelect2Type]:
        adapter = CityAdapter()
        adapter.user_id = None
        if results := await adapter.get_objects(order_by=["id"]):
            return [CitySelect2Type.from_db_model(instance=city) for city in results]
        return []

    @strawberry.field()
    async def zones(self, city_id: strawberry.ID) -> list[ZoneSelect2Type]:
        adapter = ZoneAdapter()
        adapter.user_id = None
        if results := await adapter.get_objects(
            order_by=["created_at"],
            **{"city_id": city_id},
        ):
            return [ZoneSelect2Type.from_db_model(instance=zone) for zone in results]
        return []

    @strawberry.field()
    async def specializations(self) -> list[SpecializationSelect2Type]:
        adapter = SpecializationAdapter()
        adapter.user_id = None
        if results := await adapter.get_objects(order_by=["created_at"]):
            return [
                SpecializationSelect2Type.from_db_model(instance=specialization)
                for specialization in results
            ]
        return []

    @strawberry.field()
    async def languages(self) -> list[LanguageSelect2Type]:
        adapter = LanguageAdapter()
        adapter.user_id = None
        if results := await adapter.get_objects(order_by=["created_at"]):
            return [
                LanguageSelect2Type.from_db_model(instance=language)
                for language in results
            ]
        return []


@strawberry.type()
class ProfessionalQueries:
    @strawberry.field()
    async def get_professional_list(
        self, input: QueryListUserInput
    ) -> list[ProfessionalType]:
        _input = input.to_pydantic()
        adapter = UserAdapter()

        kwargs = {
            "user_carreer_set__carreer_id": _input.carreer,
            "user_carreer_set__service_method__in": {
                _input.service_method_enum,
                psychology_constants.PRESENTIAL_VIRTUAL,
            },
            "is_verified_profile": True,
        }

        if city := _input.city:
            kwargs["user_zone_set__zone__city_id"] = city
        if zone := _input.zone:
            kwargs["user_zone_set__zone__id"] = zone

        ordering = [
            "user_carreer_set__carreer_id",
            "user_carreer_set__service_method",
            ## por pagos MENSUAL - ANUAL
            "type",
            ## por pagos de tipo de plan: BASIC - PREMIUM - VIP
            "membership_plan",
            ##
            "user_zone_set__zone__city_id",
            "user_zone_set__zone_id",
        ]

        if results := await adapter.get_objects(order_by=ordering, **kwargs):
            return [
                ProfessionalType.from_db_models(instance=professional)
                for professional in results
            ]
        return []

    @strawberry.field()
    async def get_professional(
        self,
        input: QueryRetrieveUserInput,
    ) -> ProfessionalType | None:
        adapter = UserAdapter()
        kwargs = {
            "id": input.original_id,
            "is_verified_profile": True,
        }
        if result := await adapter.get_object(**kwargs):
            return ProfessionalType.from_db_models(instance=result)

    @strawberry.field()
    async def get_membership_plans(self) -> list[MembershipPriceType]:
        adapter = MembershipPriceAdapter()
        kwargs = dict(
            membership__membership_plan__in=[
                psychology_constants.PREMIUM_PLAN,
                psychology_constants.BASIC_PLAN,
                # psychology_constants.VIP_PLAN,
            ],
            is_active=True,
            is_deleted=False,
        )
        results = await adapter.get_objects(
            order_by=["id"],
            **kwargs,
        )

        return [
            MembershipPriceType.from_db_model(instance=membership)
            for membership in results
        ]
