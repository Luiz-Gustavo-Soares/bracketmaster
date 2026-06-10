from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile, edit_profile
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='users/registration/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', register_view, name='register'),

    path('perfil/<str:username>/', profile, name='profile_view'),
    path('profile/edit', edit_profile, name='edit_profile'),
    
# 1. Tela onde o utilizador introduz o e-mail para recuperar a senha
    path(
        'senha/redefinir/',
        auth_views.PasswordResetView.as_view(
            template_name='users/registration/password_reset_form.html',
            email_template_name='users/registration/password_reset_email.html',
            subject_template_name='users/registration/password_reset_subject.txt'
        ),
        name='password_reset'
    ),
    
    # 2. Tela exibida após o envio do e-mail
    path(
        'senha/redefinir/enviado/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    
    # 3. O link seguro que o utilizador clica no e-mail
    path(
        'senha/redefinir/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    
    # 4. Tela final avisando que a senha foi alterada com sucesso
    path(
        'senha/redefinir/concluido/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]