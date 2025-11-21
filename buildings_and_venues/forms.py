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
        fields = ['name', 'street']
        labels = {
            'name': 'Building Name:'
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
        }

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'type', 'capacity', 'venue_floor_area', 'under_renovation', 'building']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter venue name'
            }),
            'type': forms.TextInput(attrs={
                'placeholder': 'Enter venue type'
            }),
            'capacity': forms.NumberInput(attrs={
                'min': 1
            }),
            'venue_floor_area': forms.NumberInput(attrs={
                'min': 1
            }),
            'under_renovation': forms.CheckboxInput(),
            'building': forms.Select()
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
