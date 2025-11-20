from django.urls import path
from .views import homepage

urlpatterns = [
    path('home/', homepage, name='homepage'),
]

app_name = 'buildings_and_venues'