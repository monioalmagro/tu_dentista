# Third-party Libraries
import strawberry

# Own Libraries
from apps.psychology.schema.types.user import ProfessionalType
from utils.graph.responses import DEFAULT_ERROR_TYPES

CreateNewProfessionalFragment = strawberry.union(
    "NewProfessionalFragment",
    types=(ProfessionalType,) + DEFAULT_ERROR_TYPES,
)
