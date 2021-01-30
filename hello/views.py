from django.shortcuts import render
from django.http import HttpResponse
import requests
from facebook_scraper import get_posts

from .models import Greeting

# Create your views here.
def index(request):
    text = ''

    for post in get_posts('monfortedelcid', pages=1):
        text += post['text']

    return HttpResponse('<pre>' + text + '</pre>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
