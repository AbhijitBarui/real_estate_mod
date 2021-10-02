from django.shortcuts import render
from .models import Testimo

def index(request):
    testimo = Testimo.objects.order_by('-review_date')
    context = {
        'testimo': testimo,
    }
    return render(request, 'testimo/testimo.html', context)
