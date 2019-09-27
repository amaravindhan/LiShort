from django.urls import path
from . import views

app_name = 'urlshortner'

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:sh_url>', views.short_redirect_lookup, name='shlookup')
]
