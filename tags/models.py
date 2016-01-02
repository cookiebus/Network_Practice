# coding: utf-8
from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    parent = models.OneToOneField("self", null=True, blank=True, related_name='parent_tag')

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.name
