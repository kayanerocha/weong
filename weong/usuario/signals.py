from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Ong

@receiver(post_save, sender=User)
def create_user_ong(sender, instance, created, **kwargs):
    if created:
        Ong.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_ong(sender, instance, **kwargs):
    instance.ong.save()