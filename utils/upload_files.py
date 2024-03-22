# Standard Libraries
import os
import uuid

# Own Libraries
from config.enviroment_vars import settings


def upload_user_image_profile(obj, filename):
    f, ext = os.path.splitext(filename)
    _uuid = uuid.uuid1()
    url = "user-image-profile/%(uuid)s/%(name)s%(ext)s" % {
        "uuid": _uuid.time_low,
        "name": f,
        "ext": ext,
    }
    if settings.DEBUG:
        url = "test/%s" % url
    return url


def upload_attachment_file(obj, filename):
    f, ext = os.path.splitext(filename)
    _uuid = uuid.uuid1()
    url = "user-attachment/%(uuid)s/%(name)s%(ext)s" % {
        "uuid": _uuid.time_low,
        "name": f,
        "ext": ext,
    }
    if settings.DEBUG:
        url = "test/%s" % url
    return url
