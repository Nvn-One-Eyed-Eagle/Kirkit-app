from django.shortcuts import render
from .models import player

# Create your views here.
from django.http import HttpResponse

def home(request):
    profile = player.objects.all()
    return render(request,"home.html",{"profile":profile} )