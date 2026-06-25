from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image, ImageDraw, ImageFilter
from shutil import copyfile

from hotel.models import (
    Amenity,
    FAQ,
    GalleryImage,
    HeroSlide,
    NearbyAttraction,
    Room,
    RoomGalleryImage,
    ServiceCard,
    ShowcaseSection,
    SiteSettings,
    Testimonial,
)

DEFAULT_IMAGE_MAP = {
    "rumelihan-hero.jpg": "02.webp",
    "single-room.jpg": "05.webp",
    "double-room.jpg": "06.webp",
    "family-room.jpg": "07.webp",
    "vip-triple-room.jpg": "15.webp",
    "gallery-detail.jpg": "03.webp",
    "gallery-hotel.jpg": "04.webp",
    "gallery-beyoglu.jpg": "11.webp",
    "gallery-room.jpg": "12.webp",
    "gallery-istanbul.jpg": "14.webp",
    "gallery-calm.jpg": "17.webp",
}


class Command(BaseCommand):
    help = "Create default Rumelihan Hotel content."

    def create_seed_image(self, filename, label, size=(1400, 950)):
        optimized_name = DEFAULT_IMAGE_MAP.get(filename)
        if optimized_name:
            source = settings.BASE_DIR / "static" / "images" / "optimized" / optimized_name
            target = settings.MEDIA_ROOT / "optimized" / optimized_name
            if source.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                copyfile(source, target)
                return f"optimized/{optimized_name}"

        path = settings.MEDIA_ROOT / "seed" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        static_source = settings.BASE_DIR / "static" / "images" / "placeholders" / filename
        if static_source.exists():
            copyfile(static_source, path)
            return f"seed/{filename}"
        if path.exists():
            return f"seed/{filename}"

        width, height = size
        image = Image.new("RGB", size, "#062B24")
        draw = ImageDraw.Draw(image)
        for y in range(height):
            ratio = y / max(height - 1, 1)
            r = int(3 + ratio * 8)
            g = int(27 + ratio * 24)
            b = int(23 + ratio * 18)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        glow = Image.new("RGBA", size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse((width * 0.52, height * 0.08, width * 1.12, height * 0.72), fill=(212, 175, 55, 34))
        glow_draw.rectangle((width * 0.08, height * 0.16, width * 0.92, height * 0.84), outline=(212, 175, 55, 120), width=4)
        glow_draw.rectangle((width * 0.12, height * 0.20, width * 0.88, height * 0.80), outline=(216, 199, 161, 70), width=1)
        glow = glow.filter(ImageFilter.GaussianBlur(1.6))
        image = Image.alpha_composite(image.convert("RGBA"), glow)

        draw = ImageDraw.Draw(image)
        draw.line((width * 0.25, height * 0.50, width * 0.75, height * 0.50), fill=(212, 175, 55, 160), width=2)
        draw.text((width * 0.12, height * 0.42), label.upper(), fill=(245, 235, 210, 230))
        draw.text((width * 0.12, height * 0.48), "RUMELIHAN HOTEL", fill=(212, 175, 55, 230))
        image.convert("RGB").save(path, quality=92)
        return f"seed/{filename}"

    def handle(self, *args, **options):
        hero_image = self.create_seed_image("rumelihan-hero.jpg", "Historic boutique stay", (1800, 1100))
        room_images = {
            "single-room": self.create_seed_image("single-room.jpg", "Single Room"),
            "double-room": self.create_seed_image("double-room.jpg", "Double Room"),
            "family-room": self.create_seed_image("family-room.jpg", "Family Room"),
            "vip-triple-room": self.create_seed_image("vip-triple-room.jpg", "VIP Triple Room"),
        }
        gallery_images = [
            self.create_seed_image("gallery-detail.jpg", "Historic Details", (1100, 1400)),
            self.create_seed_image("gallery-hotel.jpg", "Boutique Hotel", (1200, 900)),
            self.create_seed_image("gallery-beyoglu.jpg", "Beyoglu", (1000, 1300)),
            self.create_seed_image("gallery-room.jpg", "Room Textures", (1200, 1000)),
            self.create_seed_image("gallery-istanbul.jpg", "Classic Istanbul", (1000, 1350)),
            self.create_seed_image("gallery-calm.jpg", "Rumelihan Calm", (1200, 950)),
        ]

        settings = SiteSettings.get_solo()
        settings.hotel_name = "Rumelihan Hotel"
        settings.phone = "+90 541 122 67 05"
        settings.whatsapp = "905411226705"
        settings.email = "info@rumelihanhotel.com"
        settings.address_tr = "Beyoğlu, İstanbul. İstiklal Caddesi ve Taksim'e yürüme mesafesinde."
        settings.address_en = "Beyoglu, Istanbul. Within walking distance of Istiklal Street and Taksim."
        settings.instagram_url = "https://www.instagram.com/"
        settings.google_maps_link = "https://www.google.com/maps/search/?api=1&query=%C5%9Eehit%20Muhtar%2C%20%C4%B0stiklal%20Cd.%20No%3A48%2C%2034435%20Beyo%C4%9Flu%2F%C4%B0stanbul"
        settings.google_maps_embed = '<iframe src="https://maps.google.com/maps?q=%C5%9Eehit%20Muhtar%2C%20%C4%B0stiklal%20Cd.%20No%3A48%2C%2034435%20Beyo%C4%9Flu%2F%C4%B0stanbul&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>'
        settings.footer_text_tr = "Beyoğlu'nun kalbinde tarihi butik otel konforu."
        settings.footer_text_en = "Historic boutique hotel comfort in the heart of Beyoglu."
        settings.address_tr = "Şehit Muhtar, İstiklal Cd. No:48, 34435 Beyoğlu/İstanbul"
        settings.address_en = "Şehit Muhtar, İstiklal Cd. No:48, 34435 Beyoğlu/Istanbul"
        settings.save()

        HeroSlide.objects.update_or_create(
            ordering=1,
            defaults={
                "title_tr": "İstanbul'un Kalbinde Zarif Bir Konaklama",
                "title_en": "Stay in the Heart of Istanbul",
                "subtitle_tr": "İstiklal'e yakın, tarihi atmosferi ve butik ruhuyla Rumelihan Hotel.",
                "subtitle_en": "A historic boutique hotel near Istiklal with a refined old Istanbul spirit.",
                "button_text_tr": "Odaları İncele",
                "button_text_en": "Explore Rooms",
                "button_url": "/tr/rooms/",
                "image": hero_image,
                "active": True,
            },
        )

        rooms = [
            {
                "slug": "single-room",
                "title_tr": "Single Oda",
                "title_en": "Single Room",
                "short_tr": "Tek misafirler için sakin, zarif ve işlevsel oda.",
                "short_en": "A calm, elegant and practical room for solo guests.",
                "full_tr": "Single odamız, Beyoğlu keşfi veya iş seyahati için rahat bir dinlenme alanı sunar.",
                "full_en": "Our Single Room offers a comfortable retreat for Beyoglu discoveries or business travel.",
                "capacity": 1,
                "bed_tr": "Tek kişilik yatak",
                "bed_en": "Single bed",
                "features_tr": "Klima, Ücretsiz Wi-Fi, Duş, Çalışma alanı, Günlük temizlik",
                "features_en": "Air conditioning, Free Wi-Fi, Shower, Work area, Daily cleaning",
                "ordering": 1,
            },
            {
                "slug": "double-room",
                "title_tr": "Double Oda",
                "title_en": "Double Room",
                "short_tr": "Çiftler için sıcak dokularla hazırlanmış konforlu oda.",
                "short_en": "A comfortable room with warm textures for couples.",
                "full_tr": "Double odamız klasik dekorasyonu, ferah yatağı ve sakin atmosferiyle şehir sonrası dinlenmek için idealdir.",
                "full_en": "Our Double Room is ideal after a day in the city, with classic decor, a generous bed and a calm atmosphere.",
                "capacity": 2,
                "bed_tr": "Çift kişilik yatak",
                "bed_en": "Double bed",
                "features_tr": "Klima, Ücretsiz Wi-Fi, Banyo ürünleri, Gardırop, Günlük temizlik",
                "features_en": "Air conditioning, Free Wi-Fi, Bath amenities, Wardrobe, Daily cleaning",
                "ordering": 2,
            },
            {
                "slug": "family-room",
                "title_tr": "Family Oda",
                "title_en": "Family Room",
                "short_tr": "Aileler için geniş, kullanışlı ve huzurlu konaklama.",
                "short_en": "A spacious, practical and peaceful stay for families.",
                "full_tr": "Family odamız birlikte seyahat eden konuklar için rahat yerleşim, sıcak atmosfer ve pratik detaylar sunar.",
                "full_en": "Our Family Room offers comfortable layout, warm atmosphere and practical details for guests travelling together.",
                "capacity": 4,
                "bed_tr": "Çift kişilik ve tek kişilik yataklar",
                "bed_en": "Double and single beds",
                "features_tr": "Klima, Ücretsiz Wi-Fi, Aile düzeni, Oturma alanı, Günlük temizlik",
                "features_en": "Air conditioning, Free Wi-Fi, Family layout, Sitting area, Daily cleaning",
                "ordering": 3,
            },
            {
                "slug": "vip-triple-room",
                "title_tr": "VIP Triple Oda",
                "title_en": "VIP Triple Room",
                "short_tr": "Üç misafir için seçkin detaylara sahip özel oda.",
                "short_en": "A distinguished room with refined details for three guests.",
                "full_tr": "VIP Triple odamız, daha geniş kullanım ve geleneksel dokularla premium bir butik otel deneyimi sunar.",
                "full_en": "Our VIP Triple Room delivers a premium boutique experience with extra comfort and traditional textures.",
                "capacity": 3,
                "bed_tr": "Üç kişilik yatak düzeni",
                "bed_en": "Triple bed layout",
                "features_tr": "Klima, Ücretsiz Wi-Fi, Geniş oda, Banyo ürünleri, Günlük temizlik",
                "features_en": "Air conditioning, Free Wi-Fi, Spacious room, Bath amenities, Daily cleaning",
                "ordering": 4,
            },
        ]

        for item in rooms:
            Room.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "title_tr": item["title_tr"],
                    "title_en": item["title_en"],
                    "short_description_tr": item["short_tr"],
                    "short_description_en": item["short_en"],
                    "full_description_tr": item["full_tr"],
                    "full_description_en": item["full_en"],
                    "capacity": item["capacity"],
                    "bed_type_tr": item["bed_tr"],
                    "bed_type_en": item["bed_en"],
                    "size": "18-32 m2",
                    "features_tr": item["features_tr"],
                    "features_en": item["features_en"],
                    "price": "On request",
                    "main_image": room_images[item["slug"]],
                    "active": True,
                    "ordering": item["ordering"],
                },
            )
            room = Room.objects.get(slug=item["slug"])
            for index, label in enumerate(["Interior Detail", "Bathroom", "Breakfast Mood"], start=1):
                RoomGalleryImage.objects.update_or_create(
                    room=room,
                    ordering=index,
                    defaults={
                        "image": gallery_images[(item["ordering"] + index) % len(gallery_images)],
                        "alt_text_tr": f"{room.title_tr} detayı",
                        "alt_text_en": f"{room.title_en} detail",
                    },
                )

        services = [
            ("coffee", "Kahvaltı", "Breakfast", "Güne sakin ve özenli bir kahvaltıyla başlayın.", "Begin the day with a calm, carefully prepared breakfast."),
            ("wifi", "Wi-Fi", "Wi-Fi", "Otel genelinde ücretsiz kablosuz internet.", "Complimentary wireless internet throughout the hotel."),
            ("desk", "Resepsiyon", "Reception", "Şehir önerileri ve konaklama desteği.", "Local recommendations and stay assistance."),
            ("car", "Transfer", "Transfer", "Talep üzerine havalimanı transfer desteği.", "Airport transfer support upon request."),
            ("clean", "Temizlik", "Cleaning", "Düzenli oda temizliği ve özenli servis.", "Regular room cleaning and attentive service."),
            ("family", "Aile Odaları", "Family Rooms", "Birlikte seyahat eden konuklar için ferah seçenekler.", "Spacious options for guests travelling together."),
        ]
        for order, (icon, title_tr, title_en, desc_tr, desc_en) in enumerate(services, start=1):
            ServiceCard.objects.update_or_create(
                title_en=title_en,
                defaults={
                    "icon": icon,
                    "title_tr": title_tr,
                    "description_tr": desc_tr,
                    "description_en": desc_en,
                    "active": True,
                    "ordering": order,
                },
            )

        amenities = [
            ("wifi", "Güçlü Wi-Fi", "Strong Wi-Fi", "Otel genelinde hızlı bağlantı.", "Fast connection throughout the hotel."),
            ("clean", "Günlük Temizlik", "Daily Cleaning", "Odalar düzenli ve özenli şekilde hazırlanır.", "Rooms are prepared regularly and carefully."),
            ("desk", "Yerel Öneriler", "Local Advice", "Beyoğlu rotaları için yardımcı öneriler.", "Helpful tips for Beyoglu routes."),
            ("family", "Aile Konforu", "Family Comfort", "Birlikte seyahat eden konuklara uygun oda seçenekleri.", "Room options suitable for guests travelling together."),
            ("coffee", "Kahvaltı", "Breakfast", "Güne sıcak ve sade bir başlangıç.", "A warm and simple beginning to the day."),
            ("car", "Transfer Desteği", "Transfer Support", "Talep üzerine ulaşım desteği.", "Transport support upon request."),
            ("moon", "Sakin Atmosfer", "Calm Atmosphere", "Şehir içinde dingin bir konaklama hissi.", "A calm stay feeling within the city."),
            ("gold", "Butik Detaylar", "Boutique Details", "Klasik doku ve modern kullanım dengesi.", "A balance of classic texture and modern use."),
        ]
        for order, (icon, title_tr, title_en, desc_tr, desc_en) in enumerate(amenities, start=1):
            Amenity.objects.update_or_create(
                title_en=title_en,
                defaults={
                    "icon": icon,
                    "title_tr": title_tr,
                    "description_tr": desc_tr,
                    "description_en": desc_en,
                    "active": True,
                    "ordering": order,
                },
            )

        attractions = [
            ("İstiklal Caddesi", "Istiklal Street", "Beyoğlu'nun kültür, alışveriş ve yürüyüş aksı.", "Beyoglu's cultural, shopping and walking axis.", "5 dk yürüyüş", "5 min walk"),
            ("Taksim", "Taksim", "Şehrin ulaşım ve buluşma noktalarından biri.", "One of the city's transport and meeting points.", "10 dk yürüyüş", "10 min walk"),
            ("Galata Kulesi", "Galata Tower", "Tarihi siluet ve fotoğraf rotası.", "A historic skyline and photo route.", "15 dk", "15 min"),
            ("Karaköy", "Karakoy", "Kafeler, galeriler ve sahil yürüyüşleri.", "Cafes, galleries and seaside walks.", "15-20 dk", "15-20 min"),
            ("Tarihi Yarımada", "Historical Peninsula", "Sultanahmet, Ayasofya ve Kapalıçarşı rotalarına erişim.", "Access to Sultanahmet, Hagia Sophia and Grand Bazaar routes.", "Kısa ulaşım", "Short ride"),
        ]
        for order, (title_tr, title_en, desc_tr, desc_en, dist_tr, dist_en) in enumerate(attractions, start=1):
            NearbyAttraction.objects.update_or_create(
                title_en=title_en,
                defaults={
                    "title_tr": title_tr,
                    "description_tr": desc_tr,
                    "description_en": desc_en,
                    "distance_tr": dist_tr,
                    "distance_en": dist_en,
                    "image": gallery_images[order % len(gallery_images)],
                    "active": True,
                    "ordering": order,
                },
            )

        gallery_items = [
            ("Tarihi Detaylar", "Historic Details", "details"),
            ("Butik Otel Atmosferi", "Boutique Hotel Atmosphere", "hotel"),
            ("Beyoğlu Akşamları", "Beyoglu Evenings", "beyoglu"),
            ("Zarif Oda Dokuları", "Elegant Room Textures", "rooms"),
            ("Klasik İstanbul", "Classic Istanbul", "beyoglu"),
            ("Rumelihan Sakinliği", "Rumelihan Calm", "hotel"),
        ]
        for order, (title_tr, title_en, category) in enumerate(gallery_items, start=1):
            GalleryImage.objects.update_or_create(
                title_en=title_en,
                defaults={
                    "title_tr": title_tr,
                    "category": category,
                    "image": gallery_images[order - 1],
                    "active": True,
                    "ordering": order,
                },
            )

        testimonials = [
            ("Ayşe K.", "Ankara", "İstiklal'e yakınlığı ve sakin atmosferi sayesinde çok keyifli bir konaklama oldu.", "The location near Istiklal and the calm atmosphere made the stay very enjoyable."),
            ("Michael R.", "London", "Historical charm, clean rooms and warm hospitality. It felt personal, not like a chain hotel.", "Historical charm, clean rooms and warm hospitality. It felt personal, not like a chain hotel."),
            ("Elif & Can", "İzmir", "Oda temiz, dekorasyon zarif, Beyoğlu'nu yürüyerek gezmek için konum çok rahattı.", "The room was clean, the decoration elegant, and the location was very convenient for walking around Beyoglu."),
            ("Sofia M.", "Madrid", "A refined boutique mood with helpful staff and beautiful old Istanbul character.", "A refined boutique mood with helpful staff and beautiful old Istanbul character."),
            ("Murat D.", "Bursa", "Aile odası beklentimizi karşıladı; sakin, temiz ve ulaşımı kolaydı.", "The family room met our expectations; calm, clean and easy to reach."),
            ("Nina P.", "Berlin", "The hotel has a quiet elegance and a wonderful base for Galata, Karakoy and Taksim.", "The hotel has a quiet elegance and a wonderful base for Galata, Karakoy and Taksim."),
        ]
        for order, (name, location, text_tr, text_en) in enumerate(testimonials, start=1):
            Testimonial.objects.update_or_create(
                name=name,
                defaults={
                    "location": location,
                    "text_tr": text_tr,
                    "text_en": text_en,
                    "active": True,
                    "ordering": order,
                },
            )

        faqs = [
            ("rooms", "Odalar kaç kişiliktir?", "How many guests can the rooms host?", "Single, Double, Family ve VIP Triple oda seçenekleri vardır.", "Single, Double, Family and VIP Triple room options are available."),
            ("rooms", "Odalar aileler için uygun mu?", "Are the rooms suitable for families?", "Family odamız birlikte seyahat eden misafirler için daha geniş kullanım sunar.", "Our Family Room offers more generous use for guests travelling together."),
            ("rooms", "Fiyatlar sabit mi?", "Are prices fixed?", "Fiyatlar sezona ve müsaitliğe göre değişebilir; güncel bilgi için iletişime geçebilirsiniz.", "Prices may vary by season and availability; please contact us for current information."),
            ("contact", "Rezervasyon talebi kesin rezervasyon mudur?", "Is a reservation request a confirmed booking?", "Talebiniz alındıktan sonra ekip sizinle iletişime geçerek detayları netleştirir.", "After your request is received, the team contacts you to confirm details."),
            ("contact", "WhatsApp ile iletişim kurulabilir mi?", "Can I contact by WhatsApp?", "Evet, WhatsApp hattı üzerinden hızlı sorularınızı iletebilirsiniz.", "Yes, you can send quick questions through WhatsApp."),
            ("contact", "Havalimanı transferi var mı?", "Is airport transfer available?", "Talep üzerine transfer konusunda destek sağlanabilir.", "Transfer support can be arranged upon request."),
        ]
        for order, (page, q_tr, q_en, a_tr, a_en) in enumerate(faqs, start=1):
            FAQ.objects.update_or_create(
                question_en=q_en,
                defaults={
                    "page": page,
                    "question_tr": q_tr,
                    "answer_tr": a_tr,
                    "answer_en": a_en,
                    "active": True,
                    "ordering": order,
                },
            )

        ShowcaseSection.objects.update_or_create(
            pk=1,
            defaults={
                "title_tr": "Tarihin Zarafetiyle Konaklayın",
                "title_en": "Stay in the Elegance of History",
                "subtitle_tr": "Geçmişin ruhunu, bugünün konforuyla aynı çatı altında hissedin.",
                "subtitle_en": "Feel the spirit of the past under the same roof as modern comfort.",
                "image": gallery_images[3],
                "active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Rumelihan Hotel sample content created."))
