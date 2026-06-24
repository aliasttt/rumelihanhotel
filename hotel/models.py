from django.db import models
from django.urls import reverse


class OrderedActiveModel(models.Model):
    active = models.BooleanField(default=True)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["ordering", "id"]


class SiteSettings(models.Model):
    hotel_name = models.CharField(max_length=160, default="Rumelihan Hotel")
    logo = models.ImageField(upload_to="settings/", blank=True, null=True)
    phone = models.CharField(max_length=60, blank=True)
    whatsapp = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    address_tr = models.TextField(blank=True)
    address_en = models.TextField(blank=True)
    instagram_url = models.URLField(blank=True)
    google_maps_embed = models.TextField(blank=True)
    google_maps_link = models.URLField(blank=True)
    footer_text_tr = models.TextField(blank=True)
    footer_text_en = models.TextField(blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.hotel_name

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroSlide(OrderedActiveModel):
    image = models.ImageField(upload_to="hero/", blank=True, null=True)
    title_tr = models.CharField(max_length=180)
    title_en = models.CharField(max_length=180)
    subtitle_tr = models.TextField(blank=True)
    subtitle_en = models.TextField(blank=True)
    button_text_tr = models.CharField(max_length=80, blank=True)
    button_text_en = models.CharField(max_length=80, blank=True)
    button_url = models.CharField(max_length=220, blank=True)

    def __str__(self):
        return self.title_en


class Room(OrderedActiveModel):
    title_tr = models.CharField(max_length=140)
    title_en = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    short_description_tr = models.TextField()
    short_description_en = models.TextField()
    full_description_tr = models.TextField()
    full_description_en = models.TextField()
    main_image = models.ImageField(upload_to="rooms/", blank=True, null=True)
    capacity = models.PositiveIntegerField(default=2)
    bed_type_tr = models.CharField(max_length=120)
    bed_type_en = models.CharField(max_length=120)
    size = models.CharField(max_length=40, blank=True)
    features_tr = models.TextField(help_text="Virgülle ayırın.")
    features_en = models.TextField(help_text="Separate with commas.")
    price = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.title_en

    def get_absolute_url(self):
        return reverse("hotel:room_detail", kwargs={"lang": "tr", "slug": self.slug})

    def feature_list(self, lang):
        raw = self.features_tr if lang == "tr" else self.features_en
        return [item.strip() for item in raw.split(",") if item.strip()]


class RoomGalleryImage(models.Model):
    room = models.ForeignKey(Room, related_name="gallery_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="rooms/gallery/", blank=True, null=True)
    alt_text_tr = models.CharField(max_length=160, blank=True)
    alt_text_en = models.CharField(max_length=160, blank=True)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordering", "id"]

    def __str__(self):
        return f"{self.room} #{self.ordering}"


class GalleryImage(OrderedActiveModel):
    CATEGORY_CHOICES = [
        ("rooms", "Rooms"),
        ("hotel", "Hotel"),
        ("beyoglu", "Beyoglu"),
        ("details", "Details"),
    ]
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    title_tr = models.CharField(max_length=140)
    title_en = models.CharField(max_length=140)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="hotel")

    def __str__(self):
        return self.title_en


class ServiceCard(OrderedActiveModel):
    icon = models.CharField(max_length=60, blank=True, help_text="Short icon label, e.g. wifi, coffee")
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    title_tr = models.CharField(max_length=140)
    title_en = models.CharField(max_length=140)
    description_tr = models.TextField()
    description_en = models.TextField()

    def __str__(self):
        return self.title_en


class Testimonial(OrderedActiveModel):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    text_tr = models.TextField()
    text_en = models.TextField()

    def __str__(self):
        return self.name


class Amenity(OrderedActiveModel):
    icon = models.CharField(max_length=60, blank=True)
    title_tr = models.CharField(max_length=140)
    title_en = models.CharField(max_length=140)
    description_tr = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    class Meta(OrderedActiveModel.Meta):
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.title_en


class NearbyAttraction(OrderedActiveModel):
    title_tr = models.CharField(max_length=140)
    title_en = models.CharField(max_length=140)
    description_tr = models.TextField()
    description_en = models.TextField()
    distance_tr = models.CharField(max_length=80, blank=True)
    distance_en = models.CharField(max_length=80, blank=True)
    image = models.ImageField(upload_to="attractions/", blank=True, null=True)

    def __str__(self):
        return self.title_en


class FAQ(OrderedActiveModel):
    PAGE_CHOICES = [
        ("rooms", "Rooms"),
        ("contact", "Contact"),
        ("general", "General"),
    ]
    page = models.CharField(max_length=30, choices=PAGE_CHOICES, default="general")
    question_tr = models.CharField(max_length=220)
    question_en = models.CharField(max_length=220)
    answer_tr = models.TextField()
    answer_en = models.TextField()

    def __str__(self):
        return self.question_en


class ShowcaseSection(models.Model):
    title_tr = models.CharField(max_length=180, default="Tarihin Zarafetiyle Konaklayın")
    title_en = models.CharField(max_length=180, default="Stay in the Elegance of History")
    subtitle_tr = models.TextField(blank=True)
    subtitle_en = models.TextField(blank=True)
    image = models.ImageField(upload_to="showcase/", blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title_en


class ReservationRequest(models.Model):
    name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=60, blank=True)
    check_in = models.DateField(blank=True, null=True)
    check_out = models.DateField(blank=True, null=True)
    guests = models.PositiveIntegerField(default=1)
    room = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.created_at:%Y-%m-%d}"
