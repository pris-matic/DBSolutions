from django import forms
from .models import District, Building, Venue, Amenity, VenueAmenity

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['name', 'city']
        labels = {
            'name': 'District Name:',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter district name'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city'
            })
        }

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'street', 'num_floors']
        labels = {
            'name': 'Building Name:',
            'num_floors': 'Number of Floors'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter building name'
            }),
            'street': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter street'
            }),
            'num_floors': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter # of floors',
                'min': 1
			})
        }

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'type', 'capacity', 'floor', 'venue_floor_area']
        labels = {
            'name': 'Venue Name:',
            'type': 'Venue Type:',
            'capacity': 'Venue Capacity:',
            'venue_floor_area': 'Floor Area (in sqm):'
            
		}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter venue name'
            }),
            'type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter venue type'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter # of people',
                'min': 1
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter floor number',
                'min': 1
			}),
            'venue_floor_area': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter floor area',
                'min': 1
            }),
        }

class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = ['type', 'description']
        widgets = {
            'type': forms.TextInput(attrs={
                'placeholder': 'Enter amenity type'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter amenity description...'
            }),
        }

class VenueAmenityForm(forms.ModelForm):
    class Meta:
        model = VenueAmenity
        fields = ['venue', 'amenity', 'quantity']
        widgets = {
            'venue': forms.Select(),
            'amenity': forms.Select(),
            'quantity': forms.NumberInput(attrs={
                'min': 1   
            })
        }
