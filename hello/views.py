from django.shortcuts import render
from django.http import HttpResponse
import requests
from facebook_scraper import get_posts

from .models import Greeting
import re


# Delete emojis from string
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

# Clean text
def remove_special_char(text) -> str:
    text = re.sub(r'http\S+', '', text, flags=re.MULTILINE)  # Delete urls
    text = re.sub(r'#\S+', '', text)  # Delete hashtags
    text = text.replace(r'[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]', '')  # Delete special chars
    text = deEmojify(text)  # Delete emojis

    return text

# Create your views here.
def index(request):
    try:
        facebook_posts = get_posts('monfortedelcid', pages=2)        
    except:
        text = 'Ha ocurrido un error. Inténtelo de nuevo más tarde.'
    else:
        text = [remove_special_char(post['text']) for post in facebook_posts]

    return HttpResponse(text)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
