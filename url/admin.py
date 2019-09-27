from django.contrib import admin

from .models import UrlShortner
# Register your models here.

class UrlShortnerAdmin(admin.ModelAdmin):
    list_display = ['shorted_url', 'original_url', 'created']
    list_filter = ['created']

admin.site.register(UrlShortner, UrlShortnerAdmin)