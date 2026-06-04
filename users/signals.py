from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from random import choice
from users.models import Profile
from users.enums import Avatares

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    """Aciona um trigger sempre que um usuario é criado
    Criando um Profile para o usuario"""
    if created:
        Profile.objects.create(user=instance, nickname=instance.username, avatar=choice(Avatares.values))
