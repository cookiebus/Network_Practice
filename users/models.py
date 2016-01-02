# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    birthday = models.DateField(u'生日', blank=True, null=True)
    description = models.TextField(blank=True)
    friends  = models.ManyToManyField(User, blank=True)
    profile_image = models.ImageField(blank=True, upload_to='static/images/users')

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])