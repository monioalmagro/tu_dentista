from apps.psychology.admin.carreer import CarreerAdmin
from apps.psychology.admin.user_carreer import UserCarreerInline, UserCarreerAdmin
from apps.psychology.admin.user_attachment import (
    UserAttachmentAdmin,
    UserAttachmentInLine,
)

from apps.psychology.admin.contact_me import (
    ContactMeInline,
    ContactMeAdmin,
)
from apps.psychology.admin.user_language import UserLanguageInline, LanguageAdmin
from apps.psychology.admin.user_payments import UserPaymentInline, UserPaymentAdmin
from apps.psychology.admin.specialization import (
    SpecializationAdmin,
    SpecializationInline,
)
from apps.psychology.admin.admin_email_notification import AdminEmailNotificationAdmin
from apps.psychology.admin.user_specialization import UserSpecializationInline

from apps.psychology.admin.management_membership_plan import (
    MembershipAdmin,
    MembershipPriceAdmin,
    HistoryMembershipPriceInlineAdmin,
)
