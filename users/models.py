from django.db import models
from django.contrib.auth.models import User

from users.enums import Avatares
from core.models import Cidade
from users.query_sets import PerfilQuerySet


class Profile(models.Model):
    """Perfil do usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    nickname = models.CharField(max_length=50, default='')
    bio = models.TextField(blank=True, null=True)
    avatar = models.CharField(
        max_length=20,
        choices=Avatares,
        default=Avatares.AVATAR1
    )
    
    email_verificado = models.BooleanField(
        default=False
    )

    objects = PerfilQuerySet.as_manager()

    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.PROTECT,
        related_name='perfis',
        null=True,
        blank=True
    )

    def get_avatar_path(self):
        return f"/static/avatares/{self.avatar}.png"

    def __str__(self):
        return self.user.username


class ProfileLike(models.Model):

    usuario_que_curtiu = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes_feitos'
    )

    usuario_curtido = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes_recebidos'
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'usuario_que_curtiu',
                    'usuario_curtido'
                ],
                name='unique_profile_like'
            )
        ]
