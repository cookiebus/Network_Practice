# coding: utf-8
from django.db import models
from tags.models import Tag
from users.models import User
from datetime import datetime
from datetime import timedelta

# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User)
    problem_image = models.ImageField(blank=True, upload_to='images/problems')
    description = models.TextField(blank=True)
    up = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    x = models.IntegerField(default=0, blank=True)
    y = models.IntegerField(default=0, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    position = models.TextField(blank=True)
    class Meta:
        ordering = ('id', )

    def __str__(self):
        return "(%s)" % self.id
