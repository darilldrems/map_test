from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Address(models.Model):
	latitude = models.DecimalField(max_digits=9, decimal_places=6)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)
	address = models.TextField()

class FusionTable(models.Model):
	table_id = models.TextField()