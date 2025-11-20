from django.urls import path
from .views import homepage, admin_dashboard

urlpatterns = [
    path('home/', homepage, name='homepage'),
    path('home/dashboard/', admin_dashboard, name='admin_dashboard')
]

app_name = 'buildings_and_venues'