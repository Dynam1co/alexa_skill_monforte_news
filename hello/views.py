from django.shortcuts import render
from django.http import HttpResponse
import requests
from facebook_scraper import get_posts

from .models import Greeting
import re

def deEmojify(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def remove_special_char(text) -> str:
    text = text.replace(r'http\S+', '')
    text = text.replace(r'www.[^ ]+', '')

    text = text.replace(r'[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]', '')
    text = deEmojify(text)

    return text

# Create your views here.
def index(request):
    text = ''

    for post in get_posts('monfortedelcid', pages=1):
        fb_text = remove_special_char(post['text'])

        text += '<p>' + fb_text + '</p>'

    return HttpResponse(text)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
