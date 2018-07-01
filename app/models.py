# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Olympics(models.Model):
    rank = models.IntegerField(blank=True, null=True)
    country = models.CharField(primary_key=True, max_length=100)
    short_name = models.CharField(max_length=10, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    gold = models.IntegerField(blank=True, null=True)
    silver = models.IntegerField(blank=True, null=True)
    bronze = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Olympics'
