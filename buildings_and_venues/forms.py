from django import forms
from .models import District, Building, Venue, Amenity, VenueAmenity
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

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
    def __init__(self, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        # Business rule - prevents floors from being edited once building is created
        if instance and instance.pk:
            self.fields['num_floors'].disabled = True
            self.fields['num_floors'].widget.attrs['readonly'] = True

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

    def __init__(self, *args, **kwargs):
        building = kwargs.pop('building', None)  # Pass building from view
        super().__init__(*args, **kwargs)
        
        # If editing existing venue, get building from instance
        if self.instance and self.instance.pk and hasattr(self.instance, 'building'):
            building = self.instance.building
        
        # store building for validation later
        if building:
            self.building = building
    
    def clean_floor(self):
        floor = self.cleaned_data.get('floor')
        
        # Server-side validation
        if hasattr(self, 'building') and floor:
            if floor > self.building.num_floors:
                raise forms.ValidationError(
                    f'Floor number cannot exceed {self.building.num_floors} '
                    f'(selected building has only {self.building.num_floors} floors).'
                )
        
        return floor

class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = ['type', 'description']
        labels = {
            'type': 'Amenity Type:',
		}
        widgets = {
            'type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amenity type'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amenity description...'
            }),
        }

class VenueAmenityForm(forms.ModelForm):
    class Meta:
        model = VenueAmenity
        fields = ['amenity', 'quantity']
        widgets = {
            'amenity': forms.Select(),
            'quantity': forms.NumberInput(attrs={
                'min': 1   
            })
        }

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',  
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )