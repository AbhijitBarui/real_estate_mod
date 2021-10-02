from typing import List
from decouple import config
from django.shortcuts import get_object_or_404, redirect, render
from requests import api

from listings.forms import ListingForm
from .models import Listing
from listings.choices import state_choices, bedroom_choices, price_choices
import requests
from urllib.parse import urlencode

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published = True)
    context = {
        'listings': listings,
    }
    return render(request, 'listings/listings.html', context)


def listing(request,listing_id):
    
    lesting = get_object_or_404(Listing, pk=listing_id)

    if lesting.lat == 0.0 and lesting.lng == 0.0:
        address = f"{lesting.address} {lesting.city} {lesting.state}"
        data_type = "json"
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
        api_key = config('api_key')
        params = {"address": {address}, 'key': api_key}
        format = "https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY"
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)
            
        def extract_lat_lng():
            if r.status_code in range(200, 299):
                try:
                    latlng = r.json()['results'][0]['geometry']['location']
                    return latlng
                except:
                    pass
            else:
                return {}
        
        lesting.lat = extract_lat_lng().get('lat')
        lesting.lng = extract_lat_lng().get('lng')
        lesting.save()


    listing = get_object_or_404(Listing, pk=listing_id)
    api_key = config('api_key')
    context = {
        'listing': listing,
        'api_key': api_key,
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    #keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    #City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
    
    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list=queryset_list.filter(state__iexact=state)
    
    #Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list=queryset_list.filter(bedrooms__lte=bedrooms)
    
    #price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list=queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET,
    }
    return render(request, 'listings/search.html', context)

def getform(request):
    form = ListingForm
    return render(request, 'listings/list_form.html', {'form':form})

def postform(request):
    form = ListingForm(request.POST)
    if form.is_valid():
        form.save()
    return render(request, 'listings/list_form.html')