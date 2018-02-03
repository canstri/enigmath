from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from django.utils.text import slugify
from markdown_deux import markdown
#from comments.models import Comment
from django.utils.safestring import mark_safe
from transliterate import translit, get_available_language_codes
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.DecimalField(null = True, max_digits=3, decimal_places=0)
    school = models.TextField(blank = True,null = True)
    birthdate = models.DateField(null = True, blank = True)


    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"user": self.user})

    """
    @property
    def comments(self):
        qs = Comment.objects.filter_by_author(self.user)
        return qs
    """
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()