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

def add_building(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BuildingForm()
    
    return render(request, 'buildings_and_venues/add_building.html', {
        'building_form': form
    })

def add_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = VenueForm()
    
    return render(request, 'buildings_and_venues/add_venue.html', {
        'venue_form': form
    })

def add_amenity(request):
    if request.method == 'POST':
        form = AmenityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = AmenityForm()
    
    return render(request, 'buildings_and_venues/add_amenity.html', {
        'amenity_form': form
    })

def detailed_venue(request, id):
    chosen_venue = Venue.objects.get(id=id)
    neighboring_venues = Venue.objects.filter(building=chosen_venue.building)
    amenities = VenueAmenity.objects.filter(venue=chosen_venue)
    
    return render(request, 'buildings_and_venues/detailed_venue.html', {
        'venue': chosen_venue,
        'neighboring_venues': neighboring_venues,
        'amenities': amenities 
    })