from django.db import models

class Key(models.Model):
    key = models.CharField(max_length=20)
    value = models.IntegerField()
