from django.urls import path
from .views import homepage, admin_dashboard, add_building, add_venue, add_amenity

urlpatterns = [
    path('home/', homepage, name='homepage'),
    path('home/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('home/dashboard/add_building/', add_building, name='add_building'),
    path('home/dashboard/add_venue/', add_venue, name='add_venue'),
    path('home/dashboard/add_amenity/', add_amenity, name='add_amenity'),
]

app_name = 'buildings_and_venues'