# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import shortuuid

from django.db import models
from django.contrib.postgres.fields import JSONField 

# Create your models here.
class Client(models.Model):
    name = models.CharField('Client Name', max_length=50)
    uuid = models.CharField("UUID", max_length=50, blank=True, null=True)

class CRequest(models.Model):
    uuid = models.CharField("UUID", max_length=50)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    data = JSONField()
    created = models.DateTimeField(auto_now_add=True)