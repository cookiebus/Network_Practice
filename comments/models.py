# coding: utf-8
from django.db import models
from users.models import User
from problems.models import Problem


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_set')
    reply_user = models.ForeignKey(User, blank=True, null=True, related_name='reply_user')
    problem = models.ForeignKey(Problem)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return "(%s)" % self.id
