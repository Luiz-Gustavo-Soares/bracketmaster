from django.db import models
from django.conf import settings
from users.enums import Avatares

class Profile(models.Model):
    """Perfil do usuario"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    nickname = models.CharField(max_length=50, default='')
    bio = models.TextField(blank=True, null=True)
    avatar = models.CharField(
        max_length=20,
        choices=Avatares,
        default=Avatares.AVATAR1
    )
    
    def get_avatar_path(self):
        return f"/static/avatares/{self.avatar}.png"

    def __str__(self):
        return self.user.username

