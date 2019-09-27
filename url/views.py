from django.shortcuts import render, redirect, get_object_or_404
from .models import UrlShortner
from django.core.validators import URLValidator, EmailValidator
from slugify import slugify
import random, string
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def sendMail(short_url, email):
    message = """Hi, 
    Your url was successfully shortened from LiShort, this is the link: {}/{}

With Regards,
LiShort Team""".format(settings.ALLOWED_HOSTS[0],short_url)                
    send_mail(
        'URL Shortened Successfully',
        message,
        'LiShort@volleads.com',
        [email],
        fail_silently=False,
    )

def random_string(url_len = 6):
    """Generate a random string of fixed length """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(url_len))

def home(request):
    short_url = ""
    error = ""
    if request.method == "POST":
        url = request.POST.get('url')
        email = request.POST.get('email')
        keyword = request.POST.get('unique_word')
        url = url.strip()
        exists = URLValidator()
        email_valid = EmailValidator()
        try:
            exists(url)
            if keyword == "":
                shorten_url = random_string()
                try:
                    al_present = UrlShortner.objects.get(shorted_url=shorten_url)
                    shorten_url = random_string(7)
                    add_new = UrlShortner.objects.create(shorted_url=shorten_url, original_url=url)
                    short_url = shorten_url
                except UrlShortner.DoesNotExist:
                    add_new = UrlShortner.objects.create(shorted_url=shorten_url, original_url=url)
                    short_url = shorten_url
            else:
                shorten_url = slugify(keyword)
                try:
                    al_present = UrlShortner.objects.get(shorted_url=shorten_url)
                    error = 'Keyword already present. Try another'
                except UrlShortner.DoesNotExist:
                    add_new = UrlShortner.objects.create(shorted_url=shorten_url, original_url=url)
                    short_url = shorten_url
        except:
            error = 'Enter Valid URL!!'
        
        if error == "":
            try:
                email_valid(email)
                sendMail(short_url, email)
            except:
                error = 'Enter Valid Email-id!!'
                
        
    return render(request, 'url/index.html', {'short_url': short_url, 'error': error})

def short_redirect_lookup(request, sh_url):
    lishort = get_object_or_404(UrlShortner, shorted_url = sh_url)
    Ourl = lishort.original_url
    return redirect(Ourl)