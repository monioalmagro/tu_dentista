# Standard Libraries
import logging
from typing import List

# Own Libraries
from apps.core.models import AuthUser
from apps.psychology.models import UserAttachment
from utils.adapter import ModelAdapter
from utils.database import async_database

logger = logging.getLogger(__name__)


class UserAttachmentAdapterBase(ModelAdapter):
    model_class = UserAttachment

    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> List[UserAttachment]:
        kwargs["is_active"] = True
        kwargs["created_by_id"] = self.user_id
        kwargs["is_deleted"] = False
        return super().get_objects(limit, offset, order_by, **kwargs)

    def get_object(self, **kwargs) -> UserAttachment | None:
        kwargs["is_active"] = True
        kwargs["created_by_id"] = self.user_id
        kwargs["is_deleted"] = False
        return super().get_object(**kwargs)


class UserAttachmentAdapter(UserAttachmentAdapterBase):
    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> List[UserAttachment]:
        kwargs["created_by_id"] = self.user_id
        return super().get_objects(limit, offset, order_by, **kwargs)

    def get_object(self, **kwargs) -> UserAttachment | None:
        kwargs["created_by_id"] = self.user_id
        return super().get_object(**kwargs)


class EditableUserAttachmentAdapter(UserAttachmentAdapterBase):
    @async_database()
    def associate_attachment_to_user(
        self,
        user: AuthUser,
        attachment_id_list: list[int] = None,
    ):
        if user_attachment_id_list := attachment_id_list or []:
            self.get_queryset(
                id__in=user_attachment_id_list,
                created_by__isnull=True,
            ).update(created_by=user)
