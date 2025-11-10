from django.shortcuts import render

# Create your views here.

def homepage(request):
    return render(request,'buildings_and_venues/homepage.html')