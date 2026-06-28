from django.core.management.base import BaseCommand

from hotel.models import SiteSettings


class Command(BaseCommand):
    help = "Update Rumelihan Hotel contact, WhatsApp, address and map settings."

    def handle(self, *args, **options):
        settings = SiteSettings.get_solo()
        settings.phone = "+90 541 122 67 05"
        settings.whatsapp = "905411226705"
        settings.email = "Booking@rumelihanhotel.com"
        settings.address_tr = "Şehit Muhtar, İstiklal Cd. No:48, 34435 Beyoğlu/İstanbul"
        settings.address_en = "Şehit Muhtar, İstiklal Cd. No:48, 34435 Beyoğlu/Istanbul"
        settings.google_maps_link = (
            "https://www.google.com/maps/search/?api=1&query="
            "%C5%9Eehit%20Muhtar%2C%20%C4%B0stiklal%20Cd.%20No%3A48%2C%2034435%20Beyo%C4%9Flu%2F%C4%B0stanbul"
        )
        settings.google_maps_embed = (
            '<iframe src="https://maps.google.com/maps?q='
            "%C5%9Eehit%20Muhtar%2C%20%C4%B0stiklal%20Cd.%20No%3A48%2C%2034435%20Beyo%C4%9Flu%2F%C4%B0stanbul"
            '&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>'
        )
        settings.save()
        self.stdout.write(self.style.SUCCESS("Site contact information updated."))
