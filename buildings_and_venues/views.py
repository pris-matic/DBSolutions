from django.shortcuts import render, redirect
from django.db.models import Q
from .models import District, Building, Venue, Amenity, VenueAmenity
from .forms import DistrictForm, BuildingForm, VenueForm, AmenityForm, VenueAmenityForm, CustomSignupForm, CustomLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

def homepage(request):
    return render(request,'buildings_and_venues/homepage.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
                return redirect(next_url)
    else:
        form = CustomLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('buildings_and_venues:homepage')
    else:
        form = CustomSignupForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

@login_required
def admin_dashboard(request):
    buildings = Building.objects.select_related('district').prefetch_related('venues').all()
    cities = District.objects.values_list('city', flat=True).distinct().order_by('city')
    districts = District.objects.all().order_by('name')

    search = request.GET.get('search', '')
    city_filter = request.GET.get('city', '')
    district_filter = request.GET.get('district', '')
    
    if search:
        buildings = buildings.filter(Q(name__icontains=search) | Q(venues__name__icontains=search)).distinct()
    
    if city_filter and not city_filter == 'All Cities':
        buildings = buildings.filter(district__city=city_filter)

    if district_filter and not district_filter == 'All Districts':
        buildings = buildings.filter(district__id=district_filter)
        district_filter = int(district_filter)

    return render(request, 'buildings_and_venues/admin_dashboard.html', {
        'buildings': buildings,
        'cities': cities,
        'districts': districts,
        'current_search': search,
        'current_city': city_filter,
        'current_district': district_filter
    })

@login_required
def add_building(request):
    districts = District.objects.all()
    
    district_form = DistrictForm(prefix='district')
    building_form = BuildingForm(prefix='building')
    
    if request.method == 'POST':
        district_option = request.POST.get('district_option')
        if district_option == 'new':
            district_form = DistrictForm(request.POST, prefix='district')
            if district_form.is_valid():
                district = district_form.save()
                building_form = BuildingForm(request.POST, prefix='building')
                if building_form.is_valid():
                    building = building_form.save(commit=False)
                    building.district = district
                    building.save()
                    return redirect('buildings_and_venues:admin_dashboard')
        else:
            building_form = BuildingForm(request.POST, prefix='building')
            chosen_district_id = request.POST.get('district')
            chosen_district = District.objects.get(id=chosen_district_id)
            if building_form.is_valid():
                building = building_form.save(commit=False)
                building.district = chosen_district
                building.save()
                return redirect('buildings_and_venues:admin_dashboard')

    return render(request, 'buildings_and_venues/add_building.html', {
        'districts': districts,
        'district_form': district_form,
        'building_form': building_form,
    })

@login_required
def edit_building(request, id):
    building = Building.objects.get(id=id)
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            return redirect('buildings_and_venues:admin_dashboard')
    else:
        form = BuildingForm(instance=building)
    
    return render(request, 'buildings_and_venues/edit_building.html', {
        'building_form': form,
        'building': building
    })

@login_required
def add_venue(request):
    buildings = Building.objects.all()
    amenities = Amenity.objects.all()
    if request.method == 'POST':
        chosen_building_id = request.POST.get('building')
        chosen_building = Building.objects.get(id=chosen_building_id)
        form = VenueForm(request.POST, building=chosen_building)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.building = chosen_building
            if request.POST.get('under_renovation') == 'yes':
                venue.under_renovation = True
            else:
                venue.under_renovation = False
            venue.save()

            return redirect('buildings_and_venues:detailed_venue', id=venue.id)
    else:
        form = VenueForm()

    return render(request, 'buildings_and_venues/add_venue.html', {
        'venue_form': form,
        'buildings': buildings,
        'amenities': amenities
    })

@login_required
def edit_venue(request, id):
    venue = Venue.objects.get(id=id)
    if request.method == 'POST':
        form = VenueForm(request.POST, instance=venue, building=venue.building)
        if form.is_valid():
            updated_venue = form.save(commit=False)
            if request.POST.get('under_renovation') == 'yes':
                venue.under_renovation = True
            else:
                venue.under_renovation = False
            updated_venue.save()
            return redirect('buildings_and_venues:detailed_venue', id=id)
    else:
        form = VenueForm(instance=venue, building=venue.building)
    
    return render(request, 'buildings_and_venues/edit_venue.html', {
        'venue_form': form,
        'venue': venue
    })

@login_required
def detailed_venue(request, id=1):
    chosen_venue = Venue.objects.get(id=id)
    venue_amenities = VenueAmenity.objects.filter(venue=chosen_venue)
    
    if request.method == 'POST':
        chosen_venue.delete()
        return redirect('buildings_and_venues:admin_dashboard')

    return render(request, 'buildings_and_venues/detailed_venue.html', {
        'venue': chosen_venue,
        'venue_amenities': venue_amenities,
    })

@login_required
def add_amenity(request):
    if request.method == 'POST':
        form = AmenityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('buildings_and_venues:admin_dashboard')
    else:
        form = AmenityForm()
    
    return render(request, 'buildings_and_venues/add_amenity.html', {
        'amenity_form': form
    })

@login_required
def venue_amenities(request, venue_id):
    venue = Venue.objects.get(id=venue_id)
    current_amenities = VenueAmenity.objects.filter(venue=venue)
    amenities = Amenity.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            form = VenueAmenityForm(request.POST)
            
            if form.is_valid():
                venueamenity = form.save(commit=False)
                existing_amenity = VenueAmenity.objects.filter(venue=venue, amenity=venueamenity.amenity).first()
                
                if existing_amenity:
                    existing_amenity.quantity += venueamenity.quantity
                    existing_amenity.save()
                else:
                    venueamenity.venue = venue
                    venueamenity.save()
                
                return redirect('buildings_and_venues:venue_amenities', venue_id=venue_id)

        elif action == 'decrease':
            amenity_id = request.POST.get('amenity')
            chosen_amenity = VenueAmenity.objects.filter(venue=venue, amenity_id=amenity_id).first()
            if chosen_amenity.quantity > 1:
                chosen_amenity.quantity -= 1
                chosen_amenity.save()
            
            return redirect('buildings_and_venues:venue_amenities', venue_id=venue_id)

        elif action == 'delete':
            amenity_id = request.POST.get('amenity')
            chosen_amenity = VenueAmenity.objects.filter(venue=venue, amenity_id=amenity_id).first()
            chosen_amenity.delete()

            return redirect('buildings_and_venues:venue_amenities', venue_id=venue_id)
        
        elif action == 'delete_amenity':
            amenity_id = request.POST.get('amenity')
            amenity = Amenity.objects.get(id=amenity_id)
            amenity.delete()

            return redirect('buildings_and_venues:venue_amenities', venue_id=venue_id)
            
    else:
        form = VenueAmenityForm()

    return render(request, 'buildings_and_venues/venue_amenities.html', {
        'venue': venue,
        'current_amenities': current_amenities,
        'amenities': amenities
        
    })