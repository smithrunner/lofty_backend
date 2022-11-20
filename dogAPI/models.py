from django.db import models
import urllib
import urllib.request
import os
from django.core.files import File

from exiffield.fields import ExifField

class Key(models.Model):
    key = models.CharField(max_length=20, unique=True)
    value = models.IntegerField()

class CachedImage(models.Model):
    url = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(upload_to='assets/', blank=True)
    exif = ExifField(
        source='photo',
        )

    def cache(self):
        """Store image locally if we have a URL"""

        if self.url and not self.photo:
            result = urllib.request.urlretrieve(self.url)
            self.photo.save(
                    os.path.basename(self.url),
                    File(open(result[0], 'rb'))
                    )
            self.save()
