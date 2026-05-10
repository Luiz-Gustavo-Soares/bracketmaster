from django.db import models
from django.db.models import Q
from django.conf import settings
from PIL import Image
import os


def profile_image_path(instance, filename):
    """Reformula o nome de uma imagem para user_id.extension"""
    extension = filename.split('.')[-1]

    filename = f'user_{instance.user.id}.{extension}'

    return os.path.join(
        'profiles',
        filename
    )


class Profile(models.Model):
    """Perfil do usuario"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    nickname = models.CharField(max_length=50, default='')
    bio = models.TextField(blank=True, null=True)
    profile_imagem = models.ImageField(
            upload_to=profile_image_path,
            blank=True,
            null=True,
            default='profiles/default.png'
        )
    

    def get_friends(self):
        """Retorna todos os amigos de um determinado Usuario"""
        friendships = Friendship.objects.filter(
            Q(sender=self.user) | Q(receiver=self.user),
            status=FriendshipStatus.ACEITA
        )

        friends = []

        for friendship in friendships:
            if friendship.sender == self.user:
                friends.append(friendship.receiver)
            else:
                friends.append(friendship.sender)

        return friends
    
    def is_friend(self, friend):
        """Verifica se é amigo de um determinado Usuario
        Args:
            friend: User
        Return: 
            bool
        """
        if self.user == friend:
            return False

        return Friendship.objects.filter(
            (
                Q(sender=self.user, receiver=friend) |
                Q(sender=friend, receiver=self.user)
            ),
            status=FriendshipStatus.ACEITA
        ).exists()



    def save(self, *args, **kwargs):
        """Sebrescrita do metodo de save
        Processa o upload da imagem
        """


        try:
            old_profile = Profile.objects.get(pk=self.pk)

            old_image = old_profile.profile_imagem
            new_image = self.profile_imagem

            if old_image != new_image:

                if old_image.name != 'profiles/default.png':

                    # Remove a imagem antiga se for enviada uma nova
                    if old_image and os.path.isfile(old_image.path):
                        os.remove(old_image.path)

        except Profile.DoesNotExist:
            pass

        super().save(*args, **kwargs)
        
        # Redimenciona e corta a imagem
        if self.profile_imagem:

            img = Image.open(self.profile_imagem.path)

            width, height = img.size

            min_side = min(width, height)

            left = (width - min_side) / 2
            top = (height - min_side) / 2
            right = (width + min_side) / 2
            bottom = (height + min_side) / 2
            img = img.crop((left, top, right, bottom))

            img = img.resize((300, 300))
            img.save(
                self.profile_imagem.path,
                optimize=True,
                quality=80
            )


    def __str__(self):
        return self.user.username



class FriendshipStatus(models.TextChoices):
    PENDENTE = 'P', 'Pendente'
    ACEITA = 'A', 'Aceita'
    RECUSADA = 'R', 'Recusada'


class Friendship(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships_sent'
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships_received'
    )

    status = models.CharField(
        max_length=1,
        choices=FriendshipStatus.choices,
        default=FriendshipStatus.PENDENTE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Impede o envio de pedidos de amizade duplicada"""
        if self.sender.id > self.receiver.id:
            self.sender, self.receiver = self.receiver, self.sender

        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sender', 'receiver'],
                name='unique_friendship'
            )
        ]