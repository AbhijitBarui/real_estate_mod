from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search'),
    path('getform', views.getform, name='getform'),
    path('postform', views.postform, name='postform'),
]