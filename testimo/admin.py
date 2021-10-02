from django.contrib import admin
from .models import Testimo

class TestimoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'listing_title', 'review_date')
    list_display_links = ('id', 'listing_title')
    search_fields = ('name', 'listing_title')
    list_per_page = 25

admin.site.register(Testimo, TestimoAdmin)