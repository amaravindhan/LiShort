from django.db import models

# Create your models here.
class UrlShortner(models.Model):
    shorted_url = models.CharField(max_length=50)
    original_url = models.URLField(max_length=1000)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shorted_url
        
    