from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Amenity,
    DiscountCampaign,
    FAQ,
    GalleryImage,
    HeroSlide,
    NearbyAttraction,
    ReservationRequest,
    Room,
    RoomGalleryImage,
    ServiceCard,
    SiteSettings,
    ShowcaseSection,
    Testimonial,
)


admin.site.site_header = "Rumelihan Hotel Admin"
admin.site.site_title = "Rumelihan Hotel"
admin.site.index_title = "Hotel Content Management"


class ImagePreviewMixin:
    @admin.display(description="Preview")
    def image_preview(self, obj):
        image = getattr(obj, "image", None) or getattr(obj, "main_image", None) or getattr(obj, "logo", None)
        if image:
            return format_html('<img src="{}" style="width:90px;height:60px;object-fit:cover;border-radius:6px;" />', image.url)
        return "-"


@admin.register(SiteSettings)
class SiteSettingsAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("hotel_name", "phone", "email", "image_preview")
    fieldsets = (
        ("Identity", {"fields": ("hotel_name", "logo")}),
        ("Contact", {"fields": ("phone", "whatsapp", "email", "instagram_url")}),
        ("Address & Map", {"fields": ("address_tr", "address_en", "google_maps_embed", "google_maps_link")}),
        ("Footer", {"fields": ("footer_text_tr", "footer_text_en")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(HeroSlide)
class HeroSlideAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("title_en", "active", "ordering", "image_preview")
    list_editable = ("active", "ordering")
    search_fields = ("title_tr", "title_en")
    list_filter = ("active",)
    ordering = ("ordering",)


class RoomGalleryInline(ImagePreviewMixin, admin.TabularInline):
    model = RoomGalleryImage
    extra = 1
    fields = ("image", "image_preview", "alt_text_tr", "alt_text_en", "ordering")
    readonly_fields = ("image_preview",)


@admin.register(Room)
class RoomAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("title_en", "capacity", "bed_type_en", "price", "active", "ordering", "image_preview")
    list_editable = ("active", "ordering")
    prepopulated_fields = {"slug": ("title_en",)}
    search_fields = ("title_tr", "title_en", "short_description_en")
    list_filter = ("active", "capacity")
    ordering = ("ordering",)
    inlines = [RoomGalleryInline]


@admin.register(GalleryImage)
class GalleryImageAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("title_en", "category", "active", "ordering", "image_preview")
    list_editable = ("active", "ordering")
    search_fields = ("title_tr", "title_en")
    list_filter = ("active", "category")
    ordering = ("ordering",)


@admin.register(ServiceCard)
class ServiceCardAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("title_en", "icon", "active", "ordering", "image_preview")
    list_editable = ("active", "ordering")
    search_fields = ("title_tr", "title_en", "description_en")
    list_filter = ("active",)
    ordering = ("ordering",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "active", "ordering")
    list_editable = ("active", "ordering")
    search_fields = ("name", "location", "text_tr", "text_en")
    list_filter = ("active",)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("title_en", "icon", "active", "ordering")
    list_editable = ("active", "ordering")
    search_fields = ("title_tr", "title_en", "description_en")
    list_filter = ("active",)
    ordering = ("ordering",)


@admin.register(NearbyAttraction)
class NearbyAttractionAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("title_en", "distance_en", "active", "ordering", "image_preview")
    list_editable = ("active", "ordering")
    search_fields = ("title_tr", "title_en", "description_en")
    list_filter = ("active",)
    ordering = ("ordering",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question_en", "page", "active", "ordering")
    list_editable = ("active", "ordering")
    search_fields = ("question_tr", "question_en", "answer_tr", "answer_en")
    list_filter = ("page", "active")
    ordering = ("page", "ordering")


@admin.register(ShowcaseSection)
class ShowcaseSectionAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("title_en", "active", "image_preview")
    search_fields = ("title_tr", "title_en", "subtitle_tr", "subtitle_en")


@admin.register(DiscountCampaign)
class DiscountCampaignAdmin(admin.ModelAdmin):
    list_display = ("title_en", "active", "show_popup", "updated_at")
    list_editable = ("active", "show_popup")
    fieldsets = (
        ("Visibility", {"fields": ("active", "show_popup")}),
        ("Turkish Content", {"fields": ("title_tr", "message_tr", "badge_text_tr", "button_text_tr")}),
        ("English Content", {"fields": ("title_en", "message_en", "badge_text_en", "button_text_en")}),
    )

    def has_add_permission(self, request):
        return not DiscountCampaign.objects.exists()


@admin.action(description="Mark selected requests as read")
def mark_as_read(modeladmin, request, queryset):
    queryset.update(is_read=True)


@admin.register(ReservationRequest)
class ReservationRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "room", "check_in", "check_out", "guests", "is_read", "created_at")
    list_filter = ("is_read", "room", "created_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("name", "email", "phone", "check_in", "check_out", "guests", "room", "message", "created_at")
    actions = [mark_as_read]
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False
