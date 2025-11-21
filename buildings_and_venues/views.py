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
        district_option = request.POST.get('district_option')
        if district_option == 'new':
            district_form = DistrictForm(request.POST)
            if district_form.is_valid():
                district = district_form.save()
                building_form = BuildingForm(request.POST)
                if building_form.is_valid():
                    building = building_form.save(commit=False)
                    building.district = district
                    building.save()
                    return redirect('admin_dashboard')
        else:
            building_form = BuildingForm(request.POST)
            if building_form.is_valid():
                building_form.save()
                return redirect('admin_dashboard')
    else:
        district_form = DistrictForm()
        building_form = BuildingForm()
    
    districts = District.objects.all()

    return render(request, 'buildings_and_venues/add_building.html', {
        'districts': districts,
        'district_form': district_form,
        'building_form': building_form,
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

def edit_venue(request, id):
    venue = Venue.objects.get(id=id)
    if request.method == 'POST':
        form = VenueForm(request.POST, instance=venue)
        if form.is_valid():
            form.save()
            return redirect('detailed_venue', id=id)
    else:
        form = VenueForm(instance=venue)
    
    return render(request, 'buildings_and_venues/edit_venue.html', {
        'venue_form': form,
        'venue': venue
    })

def detailed_venue(request, id):
    chosen_venue = Venue.objects.get(id=id)
    neighboring_venues = Venue.objects.filter(building=chosen_venue.building)
    venue_amenities = VenueAmenity.objects.filter(venue=chosen_venue)
    
    if request.method == 'POST':
        amenity_option = request.POST.get('amenity_option')
        if amenity_option == 'new':
            amenity_form = AmenityForm(request.POST)
            if amenity_form.is_valid():
                amenity = amenity_form.save()
                venue_amenity_form = VenueAmenityForm(request.POST)
                if venue_amenity_form.is_valid():
                    venueamenity = venue_amenity_form.save(commit=False)
                    venueamenity.amenity = amenity
                    venueamenity.save()
                    return redirect('detailed_venue', id=id)
        else:
            venue_amenity_form = VenueAmenityForm(request.POST)
            if venue_amenity_form.is_valid():
                venue_amenity_form.save()
                return redirect('detailed_venue', id=id)
    else:
        amenity_form = AmenityForm()
        venue_amenity_form = VenueAmenityForm()
    
    amenities = Amenity.objects.all()

    return render(request, 'buildings_and_venues/detailed_venue.html', {
        'venue': chosen_venue,
        'neighboring_venues': neighboring_venues,
        'venue_amenities': venue_amenities,
        'amenities': amenities,
        'amenity_form': amenity_form,
        'venue_amenity_form': venue_amenity_form
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

def delete_venue_amenity(request, venue_id, amenity_id):
    if request.method == 'POST':
        VenueAmenity.objects.filter(venue_id=venue_id, amenity_id=amenity_id).delete()
    return redirect('detailed_venue', id=venue_id)

def edit_venue_amenity(request, venue_id, amenity_id):
    venue_amenity = VenueAmenity.objects.get(venue_id=venue_id, amenity_id=amenity_id)
    if request.method == 'POST':
        form = VenueAmenityForm(request.POST, instance=venue_amenity)
        if form.is_valid():
            form.save()
            return redirect('detailed_venue', id=venue_id)
    else:
        form = VenueAmenityForm(instance=venue_amenity)
    
    return render(request, 'buildings_and_venues/edit_venue_amenity.html', {
        'form': form,
        'venue_amenity': venue_amenity
    })