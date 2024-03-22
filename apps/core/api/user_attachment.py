# Standard Libraries
import json
import logging
from typing import Any

# Third-party Libraries
from django.core.files import File
from django.db import DatabaseError
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

# Own Libraries
from apps.psychology.models import UserAttachment

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class RegisterUserAttachment(TemplateView):
    http_method_names = ["post", "get"]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.method.lower() == "post":
            return self.post(request=request, *args, **kwargs)
        return JsonResponse({"Error": "Method no allowed"})

    def save_file(self, request: HttpRequest, obj_list: list[UserAttachment]):
        _avatar = request.FILES.get("avatar")
        _dni = request.FILES.get("dni")
        _matricula = request.FILES.get("matricula")
        _files = [_avatar, _dni, _matricula]
        update_fields = []
        for obj, _file in zip(obj_list, _files, strict=True):
            if obj:
                if obj.content_type != UserAttachment.USER_IMAGE:
                    obj.media_file.save(_file.name, File(_file))
                    update_fields.append("media_file")
                else:
                    obj.image.save(_file.name, File(_file))
                    update_fields.append("image")

                obj.save(update_fields=update_fields)

    def saved_user_attachments(self, request: HttpRequest):
        data_post = request.POST

        avatar = request.FILES.get("avatar")
        dni = request.FILES.get("dni")
        matricula = request.FILES.get("matricula")

        _files = [avatar, dni, matricula]
        _datas = [
            json.loads(data_post.get("avatar_data")) or {},
            json.loads(data_post.get("dni_data")) or {},
            json.loads(data_post.get("matricula_data")) or {},
        ]

        user_attachments = []

        for _file, data in zip(_files, _datas, strict=True):
            user_attachments.append(
                UserAttachment(
                    description=data.get("description") or None,
                    source_content_type=data.get("source_type"),
                    name=_file.name,
                    content_type=f""".{File(_file).name.split(".")[-1]}""",
                    size=_file.size / (1024 * 1024),
                    url_path="AWS PRESIGNED URL",
                )
            ),

        return UserAttachment.objects.bulk_create(objs=user_attachments)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            _avatar = request.FILES.get("avatar")
            dni = request.FILES.get("dni")
            matricula = request.FILES.get("matricula")
            if not _avatar:
                raise AssertionError("Avatar File not found in this request")
            if not dni:
                raise AssertionError("DNI File not found in this request")
            if not matricula:
                raise AssertionError("Matricula File not found in this request")

            attachment_list = self.saved_user_attachments(request=request)
            self.save_file(request=request, obj_list=attachment_list)
            response = {
                "originalIds": [],
                "instances": [],
            }

            for attachment_instance in attachment_list:
                response["originalIds"].append(str(attachment_instance.pk))
                response["instances"].append(
                    {
                        "originalId": attachment_instance.pk,
                        "name": attachment_instance.name,
                        "attachment_path": attachment_instance.url_path,
                    }
                )

            return JsonResponse(response)
        except AssertionError as exp:
            logger.warning(f"*** {self.__class__.__name__}.post ***")
            logger.warning(f"*** VALIDATION ERROR {repr(exp)} ***")
            return JsonResponse(
                {
                    "error": str(exp),
                    "type": "VALIDATION",
                    "code": 11,
                },
            )
        except DatabaseError as exp:
            logger.warning(f"*** {self.__class__.__name__}.post ***")
            logger.warning(f"*** INTEGRITY ERROR {repr(exp)} ***")
            return JsonResponse(
                {
                    "error": str(exp),
                    "type": "INTEGRITY",
                    "code": 12,
                },
            )
        except Exception as exp:
            logger.error(f"*** {self.__class__.__name__}.post ***")
            logger.error(f"*** INTERNAL ERROR {repr(exp)} ***")
            return JsonResponse(
                {
                    "error": str(exp),
                    "type": "INTERNAL",
                    "code": 13,
                },
            )
