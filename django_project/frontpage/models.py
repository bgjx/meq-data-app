from django.db import models
from django.urls import reverse
from django.conf import settings
import geocoder

# Create your models here.
mapbox_token = settings.MAPBOX_API_TOKEN

class Site(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    address = models.TextField(null=True)
    slug = models.SlugField(max_length=255, unique=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'sites'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project-page', args=[self.slug])
    
    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_token)
        g = g.latlng # [lat, lng]
        self.latitude, self.longitude = g[0], g[1]
        return super(Site, self).save(*args, **kwargs)
    
