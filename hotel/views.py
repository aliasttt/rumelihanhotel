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
        "nearby_attractions": NearbyAttraction.objects.filter(active=True),
        "testimonials": Testimonial.objects.filter(active=True),
    }


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
            "featured_rooms": Room.objects.filter(active=True)[:3],
            "gallery_preview": GalleryImage.objects.filter(active=True)[:6],
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
    context["rooms"] = Room.objects.filter(active=True)
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
    context["room_features"] = room.feature_list(context["lang"])
    context["related_rooms"] = Room.objects.filter(active=True).exclude(pk=room.pk)[:3]
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
    context["images"] = GalleryImage.objects.filter(active=True)
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
