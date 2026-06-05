from users.models import ProfileLike
from users.services.exceptions import AltoLikeError
from django.contrib.auth.models import User

class ProfileService:

    @classmethod
    def toggle_like(cls, usuario: User, perfil: User):
        """Altera a curtida
        Args:
            usuario: usuario que está curtindo
            usuario: usuario que está sendo curtido
        Returns:
            True -> curtiu
            False -> removeu curtida
        """
        if usuario == perfil:
            raise AltoLikeError(
                "Você não pode curtir seu próprio perfil"
            )

        like = ProfileLike.objects.filter(
            usuario_que_curtiu=usuario,
            usuario_curtido=perfil
        )

        if like.exists():
            like.delete()
            return False

        ProfileLike.objects.create(
            usuario_que_curtiu=usuario,
            usuario_curtido=perfil
        )

        return True