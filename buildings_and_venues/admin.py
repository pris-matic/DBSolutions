from django.contrib import admin
from .models import Building, Venue, Amenity, Venue_amenity

class VenueInline(admin.TabularInline):
    model = Venue
    extra = 1
    fields = ('name', 'type', 'capacity', 'under_renovation',)
    show_change_link = True

class VenueAmenityInline(admin.TabularInline):
    model = Venue_amenity
    extra = 1
    autocomplete_fields = ['amenity']

class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'street', 'district', 'city',)
    search_fields = ('name', 'city', 'district',)
    inlines = [VenueInline]

class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'capacity', 'venue_floor_area', 'under_renovation', 'building',)
    list_filter = ('under_renovation', 'type', 'building',)
    search_fields = ('name', 'type', 'building__name',)
    inlines = [VenueAmenityInline]

class AmenityAdmin(admin.ModelAdmin):
    list_display = ('type', 'description',)
    search_fields = ('type',)

# TODO: do you think we should not register this, and just use inlines instead?
# I think we can opt not to na, but baka we can add the inline as well to AmenityAdmin.
class VenueAmenityAdmin(admin.ModelAdmin):
    list_display = ('venue', 'amenity', 'quantity',)
    search_fields = ('venue__name', 'amenity__type',)

admin.site.register(Building, BuildingAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(Venue_amenity, VenueAmenityAdmin)
