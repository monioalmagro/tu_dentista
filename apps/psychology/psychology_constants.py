# model UserAttachment
PREFIX_UNZIP = "unzip"
IMAGE_EXTENSIONS = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/bmp": "bmp",
}
MEDIA_EXTENSIONS = {
    "application/pdf": "pdf",
    "application/zip": "zip",
    "application/x-compressed": "zip",
    "application/x-zip-compressed": "zip",
    "multipart/x-zip": "zip",
    "application/vnd.ms-powerpoint": "ppt",
    "application/msword": "doc",
    "video/mp4": "mp4",
    "application/octet-stream": "pbix",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "apadsheetml.sheet": "xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.ms-excel": "xls",
    "application/vnd.ms-excel.sheet.macroenabled.12": "xlsm",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
    "application/x-rar-compressed": "rar",
    "application/rar": "rar",
}

# model OfficeLocation

VISIBILITY_DRAFT = 1
VISIBILITY_ACTIVE = 2
VISIBILITY_INACTIVE = 3

VISIBILITY_STATUS_CHOICES = (
    (VISIBILITY_DRAFT, "VISIBILITY_DRAFT"),
    (VISIBILITY_ACTIVE, "VISIBILITY_ACTIVE"),
    (VISIBILITY_INACTIVE, "VISIBILITY_INACTIVE"),
)

TYPE_HOUSE = 1
TYPE_OFFICE = 2
LOCATION_TYPE_CHOICES = (
    (TYPE_HOUSE, "TYPE_HOUSE"),
    (TYPE_OFFICE, "TYPE_OFFICE"),
)

# model UserCarreer

PRESENTIAL = 1
VIRTUAL = 2
PRESENTIAL_VIRTUAL = 3

SERVICE_METHOD_CHOICES = (
    (PRESENTIAL, "PRESENCIAL"),
    (VIRTUAL, "VIRTUAL"),
    (PRESENTIAL_VIRTUAL, "PRESENCIAL/VIRTUAL"),
)

INDIVIDUAL = 1
GROUPS = 2

SERVICE_MODALITY_CHOICES = (
    (INDIVIDUAL, "INDIVIDUAL"),
    (GROUPS, "GRUPAL"),
)

# model UserLanguage

ES = 1
EN = 2
IT = 3
GER = 4
FR = 5

LANG_CHOICES = (
    (ES, "ES"),
    (EN, "EN"),
    (IT, "IT"),
    (GER, "GER"),
    (FR, "FR"),
)

EASY = 1
MEDIUM = 2
HARD = 3
EXPERT = 4


LANG_LEVEL_CHOICES = (
    (EASY, "EASY"),
    (MEDIUM, "MEDIUM"),
    (HARD, "HARD"),
    (EXPERT, "EXPERT"),
)

# model

MONTHLY_PAYMENT = 1
ANNUAL_PAYMENT = 2


PAYMENT_CHOICES = (
    (MONTHLY_PAYMENT, "MONTHLY_PAYMENT"),
    (ANNUAL_PAYMENT, "ANNUAL_PAYMENT"),
)

BASIC_PLAN = 1
PREMIUM_PLAN = 2
VIP_PLAN = 3

MEMBERSHIP_PLAN_TYPE_CHOICES = (
    (BASIC_PLAN, "BASIC_PLAN"),
    (PREMIUM_PLAN, "PREMIUM_PLAN"),
    (VIP_PLAN, "VIP_PLAN"),
)

# model AdminEmailNotification

USER_PAYMENT = 1
CONTACT_ME = 2

ADMIN_EMAIL_NOTIFICATION_CONTENT_TYPE_CHOICES = (
    (USER_PAYMENT, "PAGO_DEL_USUARIO"),
    (CONTACT_ME, "MENSAJE_AL_PROFESIONAL"),
)
# model AdminEmailNotification
