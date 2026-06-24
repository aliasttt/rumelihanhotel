from django.db import migrations


def update_site_contact(apps, schema_editor):
    SiteSettings = apps.get_model("hotel", "SiteSettings")
    settings, _ = SiteSettings.objects.get_or_create(pk=1)
    settings.phone = "+90 541 122 67 05"
    settings.whatsapp = "905411226705"
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


class Migration(migrations.Migration):
    dependencies = [
        ("hotel", "0002_amenity_faq_nearbyattraction_showcasesection_and_more"),
    ]

    operations = [
        migrations.RunPython(update_site_contact, migrations.RunPython.noop),
    ]
