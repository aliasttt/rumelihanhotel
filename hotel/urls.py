from django.urls import path

from . import views


app_name = "hotel"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("rooms/", views.rooms, name="rooms"),
    path("rooms/<slug:slug>/", views.room_detail, name="room_detail"),
    path("gallery/", views.gallery, name="gallery"),
    path("services/", views.services, name="services"),
    path("location/", views.location, name="location"),
    path("contact/", views.contact, name="contact"),
]
