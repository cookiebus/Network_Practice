from django.contrib.auth.models import User
from django.db import models
from problems.models import Problem
# Create your models here.


class Favorite(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{user} liked {problem}".format(user=self.user.username, problem=self.problem.title)