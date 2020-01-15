import json
import shortuuid

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.template.defaultfilters import slugify

class Form(models.Model):
    uuid = models.CharField("ShortUUID", max_length=50, blank=True, null=True)
    name = models.CharField("Page Name", max_length=255)
    fields =  JSONField(default=[])
    configs = JSONField(default={})
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.IntegerField(blank=True, null=True)
    ftype = models.IntegerField(default=1)
    tips = JSONField(default={})    

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.uuid = shortuuid.uuid()
        super(Form, self).save(*args, **kwargs)


class Opts(models.Model):
    category = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    value = models.CharField("Value", max_length=255)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.value

class FormResponse(models.Model):
    uuid = models.CharField("ShortUUID", max_length=50, blank=True, null=True)
    form = models.PositiveIntegerField(default=1)
    response = JSONField(default={})

    def save(self, *args, **kwargs):
        if not self.id:
            self.uuid = shortuuid.uuid()
        super(FormResponse, self).save(*args, **kwargs)