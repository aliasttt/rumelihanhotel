from .models import DiscountCampaign, SiteSettings


DEFAULT_PHONE_DISPLAY = "+90 541 122 67 05"
DEFAULT_PHONE_TEL = "+905411226705"
DEFAULT_WHATSAPP = "905411226705"
DEFAULT_ADDRESS_TR = "Şehit Muhtar, İstiklal Cd. No:48, 34435 Beyoğlu/İstanbul"
DEFAULT_ADDRESS_EN = "Şehit Muhtar, İstiklal Cd. No:48, 34435 Beyoğlu/Istanbul"
DEFAULT_MAP_LINK = (
    "https://www.google.com/maps/search/?api=1&query="
    "%C5%9Eehit%20Muhtar%2C%20%C4%B0stiklal%20Cd.%20No%3A48%2C%2034435%20Beyo%C4%9Flu%2F%C4%B0stanbul"
)
DEFAULT_MAP_EMBED = (
    '<iframe src="https://maps.google.com/maps?q='
    "%C5%9Eehit%20Muhtar%2C%20%C4%B0stiklal%20Cd.%20No%3A48%2C%2034435%20Beyo%C4%9Flu%2F%C4%B0stanbul"
    '&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>'
)


def is_old_phone(value):
    return not value or "212 000" in value


def is_old_whatsapp(value):
    return not value or value == "902120000000"


def is_old_address(value):
    return not value or "Taksim" in value or "Beyoglu, Istanbul" in value


def site_settings(request):
    settings = SiteSettings.get_solo()
    lang = getattr(request, "resolver_match", None)
    lang = request.path.strip("/").split("/", 1)[0] if request else "tr"
    address = settings.address_tr if lang == "tr" else settings.address_en
    default_address = DEFAULT_ADDRESS_TR if lang == "tr" else DEFAULT_ADDRESS_EN

    campaign = DiscountCampaign.get_solo()

    return {
        "site_settings": settings,
        "discount_campaign": campaign,
        "contact_phone_display": DEFAULT_PHONE_DISPLAY if is_old_phone(settings.phone) else settings.phone,
        "contact_phone_tel": DEFAULT_PHONE_TEL if is_old_phone(settings.phone) else settings.phone.replace(" ", ""),
        "contact_whatsapp": DEFAULT_WHATSAPP if is_old_whatsapp(settings.whatsapp) else settings.whatsapp,
        "contact_address": default_address if is_old_address(address) else address,
        "contact_map_link": settings.google_maps_link or DEFAULT_MAP_LINK,
        "contact_map_embed": settings.google_maps_embed or DEFAULT_MAP_EMBED,
    }
