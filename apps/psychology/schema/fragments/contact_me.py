# Third-party Libraries
import strawberry

# Own Libraries
from apps.psychology.schema.types.contact_me import ContactMeType
from utils.graph.responses import DEFAULT_ERROR_TYPES

PublicContactMeFragment = strawberry.union(
    "ContactMeFragment",
    types=(ContactMeType,) + DEFAULT_ERROR_TYPES,
)
