from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ReservationRequestForm
from .models import (
    Amenity,
    FAQ,
    GalleryImage,
    HeroSlide,
    NearbyAttraction,
    Room,
    ServiceCard,
    ShowcaseSection,
    SiteSettings,
    Testimonial,
)


LANGS = {"tr", "en"}

OPTIMIZED_GALLERY = [
    {"path": "images/optimized/02.webp", "title_tr": "Rumelihan Lobi", "title_en": "Rumelihan Lobby", "category": "hotel"},
    {"path": "images/optimized/03.webp", "title_tr": "Tarihi Detaylar", "title_en": "Historic Details", "category": "details"},
    {"path": "images/optimized/04.webp", "title_tr": "Otel Atmosferi", "title_en": "Hotel Atmosphere", "category": "hotel"},
    {"path": "images/optimized/05.webp", "title_tr": "Butik Oda", "title_en": "Boutique Room", "category": "rooms"},
    {"path": "images/optimized/06.webp", "title_tr": "Aile Konforu", "title_en": "Family Comfort", "category": "rooms"},
    {"path": "images/optimized/07.webp", "title_tr": "Sakin Konaklama", "title_en": "Calm Stay", "category": "rooms"},
    {"path": "images/optimized/10.webp", "title_tr": "Kahvaltı", "title_en": "Breakfast", "category": "hotel"},
    {"path": "images/optimized/11.webp", "title_tr": "Beyoğlu", "title_en": "Beyoglu", "category": "beyoglu"},
    {"path": "images/optimized/12.webp", "title_tr": "Oda Işığı", "title_en": "Room Light", "category": "rooms"},
    {"path": "images/optimized/13.webp", "title_tr": "Banyo Detayı", "title_en": "Bathroom Detail", "category": "details"},
    {"path": "images/optimized/14.webp", "title_tr": "İstanbul Dokusu", "title_en": "Istanbul Texture", "category": "beyoglu"},
    {"path": "images/optimized/15.webp", "title_tr": "Rumelihan Odası", "title_en": "Rumelihan Room", "category": "rooms"},
    {"path": "images/optimized/16.webp", "title_tr": "Sessiz Detay", "title_en": "Quiet Detail", "category": "details"},
    {"path": "images/optimized/17.webp", "title_tr": "Konaklama Detayı", "title_en": "Stay Detail", "category": "hotel"},
]

ROOM_IMAGE_PATHS = [
    "images/optimized/05.webp",
    "images/optimized/06.webp",
    "images/optimized/07.webp",
    "images/optimized/15.webp",
]

ROOM_DETAIL_IMAGE_PATHS = [
    "images/optimized/13.webp",
    "images/optimized/03.webp",
    "images/optimized/10.webp",
]

ATTRACTION_IMAGE_PATHS = [
    "images/optimized/11.webp",
    "images/optimized/14.webp",
    "images/optimized/04.webp",
]


def normalize_lang(lang):
    return lang if lang in LANGS else "tr"


def page_context(lang, page_key, title_tr, title_en, description_tr, description_en):
    lang = normalize_lang(lang)
    nav = [
        ("home", "Ana Sayfa", "Home", reverse("hotel:home", kwargs={"lang": lang})),
        ("about", "Hakkımızda", "About", reverse("hotel:about", kwargs={"lang": lang})),
        ("rooms", "Odalar", "Rooms", reverse("hotel:rooms", kwargs={"lang": lang})),
        ("gallery", "Galeri", "Gallery", reverse("hotel:gallery", kwargs={"lang": lang})),
        ("services", "Hizmetler", "Services", reverse("hotel:services", kwargs={"lang": lang})),
        ("location", "Konum", "Location", reverse("hotel:location", kwargs={"lang": lang})),
        ("contact", "İletişim", "Contact", reverse("hotel:contact", kwargs={"lang": lang})),
    ]
    return {
        "lang": lang,
        "other_lang": "en" if lang == "tr" else "tr",
        "nav_items": nav,
        "active_page": page_key,
        "page_title": title_tr if lang == "tr" else title_en,
        "meta_description": description_tr if lang == "tr" else description_en,
        "amenities": Amenity.objects.filter(active=True),
        "nearby_attractions": with_optimized_attraction_images(NearbyAttraction.objects.filter(active=True)),
        "testimonials": Testimonial.objects.filter(active=True),
    }


def with_optimized_room_images(rooms):
    rooms = list(rooms)
    for index, room in enumerate(rooms):
        room.optimized_image = ROOM_IMAGE_PATHS[index % len(ROOM_IMAGE_PATHS)]
    return rooms


def attach_optimized_room_image(room):
    rooms = list(Room.objects.filter(active=True).order_by("ordering", "id"))
    index = next((i for i, item in enumerate(rooms) if item.pk == room.pk), 0)
    room.optimized_image = ROOM_IMAGE_PATHS[index % len(ROOM_IMAGE_PATHS)]
    return room


def with_optimized_attraction_images(items):
    items = list(items)
    for index, item in enumerate(items):
        item.optimized_image = ATTRACTION_IMAGE_PATHS[index % len(ATTRACTION_IMAGE_PATHS)]
    return items


def home(request, lang):
    lang = normalize_lang(lang)
    context = page_context(
        lang,
        "home",
        "Rumelihan Hotel | Beyoğlu Butik Otel",
        "Rumelihan Hotel | Boutique Hotel in Beyoglu",
        "Beyoğlu ve İstiklal'e yakın, tarihi atmosfere sahip zarif butik otel.",
        "An elegant historic boutique hotel near Istiklal in Beyoglu, Istanbul.",
    )
    context.update(
        {
            "hero_slides": HeroSlide.objects.filter(active=True),
            "featured_rooms": with_optimized_room_images(Room.objects.filter(active=True)[:3]),
            "gallery_preview": OPTIMIZED_GALLERY[:6],
            "services_preview": ServiceCard.objects.filter(active=True)[:4],
            "showcase": ShowcaseSection.objects.filter(active=True).first(),
        }
    )
    return render(request, "hotel/home.html", context)


def about(request, lang):
    context = page_context(
        lang,
        "about",
        "Rumelihan Hotel Hakkında",
        "About Rumelihan Hotel",
        "Rumelihan Hotel'in tarihi butik otel konsepti ve Beyoğlu ruhu.",
        "The historic boutique concept and Beyoglu spirit of Rumelihan Hotel.",
    )
    return render(request, "hotel/about.html", context)


def rooms(request, lang):
    context = page_context(
        lang,
        "rooms",
        "Odalar",
        "Rooms",
        "Single, Double, Family ve VIP Triple odalar.",
        "Single, Double, Family and VIP Triple rooms.",
    )
    context["rooms"] = with_optimized_room_images(Room.objects.filter(active=True))
    context["faqs"] = FAQ.objects.filter(active=True, page="rooms")
    return render(request, "hotel/rooms.html", context)


def room_detail(request, lang, slug):
    room = get_object_or_404(Room, slug=slug, active=True)
    title = room.title_tr if lang == "tr" else room.title_en
    context = page_context(
        lang,
        "rooms",
        title,
        title,
        room.short_description_tr,
        room.short_description_en,
    )
    context["room"] = room
    context["room"] = attach_optimized_room_image(room)
    context["room_detail_images"] = ROOM_DETAIL_IMAGE_PATHS
    context["room_features"] = room.feature_list(context["lang"])
    context["related_rooms"] = with_optimized_room_images(Room.objects.filter(active=True).exclude(pk=room.pk)[:3])
    return render(request, "hotel/room_detail.html", context)


def gallery(request, lang):
    context = page_context(
        lang,
        "gallery",
        "Galeri",
        "Gallery",
        "Rumelihan Hotel odaları, detayları ve Beyoğlu atmosferi.",
        "Rooms, details and Beyoglu atmosphere at Rumelihan Hotel.",
    )
    context["images"] = OPTIMIZED_GALLERY
    return render(request, "hotel/gallery.html", context)


def services(request, lang):
    context = page_context(
        lang,
        "services",
        "Hizmetler",
        "Services",
        "Kahvaltı, Wi-Fi, resepsiyon, transfer ve aile odaları.",
        "Breakfast, Wi-Fi, reception, transfer and family rooms.",
    )
    context["services"] = ServiceCard.objects.filter(active=True)
    return render(request, "hotel/services.html", context)


def location(request, lang):
    context = page_context(
        lang,
        "location",
        "Beyoğlu Konumu",
        "Beyoglu Location",
        "İstiklal, Taksim, Galata ve Tarihi Yarımada'ya yakın konum.",
        "Close to Istiklal, Taksim, Galata and the Historical Peninsula.",
    )
    context["settings_obj"] = SiteSettings.get_solo()
    return render(request, "hotel/location.html", context)


def contact(request, lang):
    lang = normalize_lang(lang)
    context = page_context(
        lang,
        "contact",
        "İletişim ve Rezervasyon",
        "Contact and Reservation",
        "Rumelihan Hotel için rezervasyon talebi oluşturun.",
        "Send a reservation request to Rumelihan Hotel.",
    )
    if request.method == "POST":
        form = ReservationRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Talebiniz alındı. En kısa sürede sizinle iletişime geçeceğiz."
                if lang == "tr"
                else "Your request has been received. We will contact you shortly.",
            )
            return redirect(reverse("hotel:contact", kwargs={"lang": lang}))
    else:
        form = ReservationRequestForm()
    context["form"] = form
    context["faqs"] = FAQ.objects.filter(active=True, page="contact")
    return render(request, "hotel/contact.html", context)
