# Third-party Libraries
import strawberry
from pydantic import BaseModel


class UserCarreerPydanticModel(BaseModel):
    user_id: strawberry.ID
    carreer_id: strawberry.ID
    service_method: int
    service_modality: int
    experience_summary: str | None = None

    class Config:
        use_enum_values = True
