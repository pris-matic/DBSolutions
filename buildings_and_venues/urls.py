from django.urls import path
from .views import homepage, admin_dashboard, add_building

urlpatterns = [
    path('home/', homepage, name='homepage'),
    path('home/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('home/dashboard/add_building/', add_building, name='add_building')
]

app_name = 'buildings_and_venues'