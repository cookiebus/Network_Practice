# coding: utf-8
from django.db import models
from tags.models import Tag
from users.models import User
from datetime import datetime
from datetime import timedelta

# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User)
    problem_image = models.ImageField(blank=True, upload_to='images/problems')
    description = models.TextField(blank=True)
    up = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    X = models.IntegerField(default=0, blank=True)
    Y = models.IntegerField(default=0, blank=True)
    # for admin
    create_at = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return "(%s)" % self.id
