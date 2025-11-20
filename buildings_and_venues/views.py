from django.shortcuts import render, redirect
from .models import District, Building, Venue, Amenity, VenueAmenity
from .forms import DistrictForm, BuildingForm, VenueForm, AmenityForm, VenueAmenityForm

def homepage(request):
    return render(request,'buildings_and_venues/homepage.html')

def admin_dashboard(request):
    buildings = Building.objects.prefetch_related('venues').all()
        
    return render(request, 'buildings_and_venues/admin_dashboard.html', {
        'buildings': buildings
    })