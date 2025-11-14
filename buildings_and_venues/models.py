from django.db import models

class District(models.Model):
    '''
    ## Represents a district which is always in one city.
    '''
    name = models.CharField(max_length=255, unique=True) # Based on assumption that district names are unique and 
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def get_city(self):
        return self.city

class Building(models.Model):
    '''
    ## The buildings that State Spaces own in which 
    ## the venues they offer their customers are located. 
    '''
    name = models.CharField(max_length=255, unique=True) # Business rule
    street = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='buildings')

    def __str__(self):
        return self.name

class Venue(models.Model):
    '''
    ## Venues that State Spaces own. 
    ## Availability of each venue depends if it is currently being renovated.
    '''
    name = models.CharField(max_length=255, unique=True) # Business rule
    type = models.CharField(max_length=255)
    capacity = models.IntegerField()
    venue_floor_area = models.IntegerField()
    under_renovation = models.BooleanField(default=False)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='venues')

    def __str__(self):
        return self.name
    
class Amenity(models.Model):
    '''
    ## Amenities that State Spaces provide for each venue/building.
    '''
    type = models.CharField(max_length=255) # name of the amenity
    description = models.TextField()

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = "Amenities"

class Venue_amenity(models.Model): # associative entity
    '''
    ## Junction table for many-to-many relationship between venues and amenities.
    '''
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.venue.name} - {self.amenity.type}"
    
    class Meta:
        verbose_name_plural = "Venue Amenities"