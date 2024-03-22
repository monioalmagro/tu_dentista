# Standard Libraries
import logging

# Third-party Libraries
import strawberry
from strawberry.types import Info

# Own Libraries
from apps.psychology.schema.fragments.contact_me import PublicContactMeFragment
from apps.psychology.schema.fragments.new_professional import (
    CreateNewProfessionalFragment,
)
from apps.psychology.schema.inputs.contact_me import MutationContactMeInput
from apps.psychology.schema.inputs.user import MutationUserInput
from apps.psychology.schema.mutations_process.user import (
    ContactProfessionalProcess,
    ContactProfessionalValidator,
    NewProfessionalProcess,
    ProfessionalValidator,
)
from apps.psychology.schema.types.contact_me import ContactMeType
from apps.psychology.schema.types.user import ProfessionalType
from utils.decorators import mutation_exception_handler

logger = logging.getLogger(__name__)


@strawberry.type()
class ProfessionalMutations:
    @strawberry.field()
    @mutation_exception_handler(log_tag="ProfessionalMutations")
    async def contact_me(
        self,
        info: Info,
        input: MutationContactMeInput,
    ) -> PublicContactMeFragment | None:
        _input = input.to_pydantic()
        validator = ContactProfessionalValidator(_input=_input)
        process = ContactProfessionalProcess(
            validator_instance=validator,
            _input=_input,
        )
        if contact_me_instance := await process.action(info=info):
            return ContactMeType.from_db_model(instance=contact_me_instance)

    @strawberry.field()
    @mutation_exception_handler(log_tag="ProfessionalMutations")
    async def new_professional(
        self,
        info: Info,
        input: MutationUserInput,
    ) -> CreateNewProfessionalFragment:
        _input = input.to_pydantic()
        validator = ProfessionalValidator(_input=_input)
        process = NewProfessionalProcess(
            validator_instance=validator,
            _input=_input,
        )

        if new_professional := await process.action(info=info):
            return ProfessionalType.from_db_models(instance=new_professional)
