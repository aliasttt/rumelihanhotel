from django.db import migrations, models


REPLACEMENTS = {
    "Ä°": "İ",
    "Ä±": "ı",
    "ÄŸ": "ğ",
    "Äž": "Ğ",
    "Ã¼": "ü",
    "Ãœ": "Ü",
    "Ã¶": "ö",
    "Ã–": "Ö",
    "Ã§": "ç",
    "Ã‡": "Ç",
    "ÅŸ": "ş",
    "Åž": "Ş",
    "Ã¢": "â",
    "Ã®": "î",
    "Ã»": "û",
    "Â": "",
}


MODEL_NAMES = [
    "SiteSettings",
    "HeroSlide",
    "Room",
    "RoomGalleryImage",
    "GalleryImage",
    "ServiceCard",
    "Testimonial",
    "Amenity",
    "NearbyAttraction",
    "FAQ",
    "ShowcaseSection",
    "DiscountCampaign",
]


def fix_text(value):
    if not isinstance(value, str):
        return value
    for bad, good in REPLACEMENTS.items():
        value = value.replace(bad, good)
    return value


def fix_model_text(apps, schema_editor):
    for model_name in MODEL_NAMES:
        model = apps.get_model("hotel", model_name)
        text_fields = [
            field.name
            for field in model._meta.fields
            if isinstance(field, (models.CharField, models.TextField, models.EmailField, models.URLField, models.SlugField))
        ]
        for obj in model.objects.all():
            changed = []
            for field_name in text_fields:
                old_value = getattr(obj, field_name)
                new_value = fix_text(old_value)
                if new_value != old_value:
                    setattr(obj, field_name, new_value)
                    changed.append(field_name)
            if changed:
                obj.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [
        ("hotel", "0004_discountcampaign"),
    ]

    operations = [
        migrations.RunPython(fix_model_text, migrations.RunPython.noop),
    ]
