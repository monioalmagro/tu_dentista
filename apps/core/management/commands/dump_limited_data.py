# Third-party Libraries
from django.core import serializers
from django.core.management.base import BaseCommand

# Own Libraries
# Own Libraries]
from apps.core.models import AuthUser, City, Country, UserZone, Zone
from apps.psychology.models import (
    AdminEmailNotification,
    Carreer,
    ContactMe,
    HistoryMembershipPrice,
    Language,
    Membership,
    MembershipPrice,
    Specialization,
    UserAttachment,
    UserCarreer,
    UserLanguage,
    UserPayment,
    UserSpecialization,
)


class Command(BaseCommand):
    help = "Export the first 500 records of MyModel"

    models = (
        (AuthUser, "AuthUser"),
        (Country, "Country"),
        (City, "City"),
        (Zone, "Zone"),
        (UserZone, "UserZone"),
        (Carreer, "Carreer"),
        (ContactMe, "ContactMe"),
        (UserAttachment, "UserAttachment"),
        (UserCarreer, "UserCarreer"),
        (Language, "Language"),
        (UserLanguage, "UserLanguage"),
        (UserPayment, "UserPayment"),
        (Specialization, "Specialization"),
        (UserSpecialization, "UserSpecialization"),
        (AdminEmailNotification, "AdminEmailNotification"),
        (HistoryMembershipPrice, "HistoryMembershipPrice"),
        (Membership, "Membership"),
        (MembershipPrice, "MembershipPrice"),
    )

    def handle(self, *args, **options):
        # Obtener los primeros 10 registros del modelo
        for model, model_name in self.models:
            first_500_records = model.objects.all().order_by("id")[:500]

            # Serializar los registros en formato JSON
            data = serializers.serialize("json", first_500_records)

            # Guardar los datos en un archivo
            with open(f"tests/fixtures/json/{model_name}.json", "w") as file:
                file.write(data)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully exported the first 500 records to model_data.json"
            )
        )
