from django.db import models


# Create your models here.

class System(models.Model):
    key = models.CharField(primary_key=True, max_length=1000)
    value = models.CharField(max_length=1000, blank=True, null=True)
