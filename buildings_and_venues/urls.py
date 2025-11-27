from django.urls import path
from .views import homepage, admin_dashboard, add_building, add_venue, add_amenity, detailed_venue, edit_venue, venue_amenities, edit_building, login_view, signup_view, logout_view
from django.contrib.auth import views

urlpatterns = [
    path('home/', homepage, name='homepage'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/add_building/', add_building, name='add_building'),
    path('dashboard/add_venue/', add_venue, name='add_venue'),
    path('dashboard/add_amenity/', add_amenity, name='add_amenity'),
    path('dashboard/venue/<int:id>', detailed_venue, name='detailed_venue'),
    path('dashboard/edit_venue/<int:id>', edit_venue, name='edit_venue'),
    path('dashboard/venue/<int:venue_id>/amenities/', venue_amenities, name='venue_amenities'),
    path('dashboard/edit_building/<int:id>', edit_building, name='edit_building'),
    path('login/', login_view, name='login'),
    path('register/', signup_view, name='register'),
    path('logout/', logout_view, name='logout'),
]

app_name = 'buildings_and_venues'