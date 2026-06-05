from users.models import Profile, ProfileLike
from users.services.exceptions import AltoLikeError, EmailValidationError
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

class ProfileService:

    @classmethod
    def email_validation(cls, uidb64, token):
        """Verifica se o uid e o token estao corretos e verifica o email do usuario"""
        uid = force_str(
                urlsafe_base64_decode(uidb64)
            )

        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.perfil.email_verificado = True
            user.perfil.save()
            return True
        
        return False



    @classmethod
    def send_mail_email_validation(cls, perfil: Profile, host: str):
        """Envia um email para a validacao de email do usuario
        Args: 
            perfil: Profile
            host: host do server
        """
        if perfil.email_verificado:
            raise EmailValidationError('Email já verificado')
        
        token = default_token_generator.make_token(perfil.user)
        uid = urlsafe_base64_encode(
            force_bytes(perfil.user.pk)
        )

        link = f"http://{host}/ativar/{uid}/{token}/"

        send_mail(
            subject="Confirme seu email",
            message=f"Clique aqui: {link}",
            from_email="noreply@site.com",
            recipient_list=[perfil.user.email]
        )


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