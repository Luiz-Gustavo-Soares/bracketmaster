from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile, edit_profile, login_view, like_profile


urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('login/', login_view, name='login'),

    path('register/', register_view, name='register'),

    path('profile/edit', edit_profile, name='edit_profile'),
    
    
    path('profile/like/<str:username>', like_profile, name='like_profile'),

    path(
        "senha/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset"
    ),

    path(
        "senha/enviado/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"
    ),

    path(
        "senha/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),

    path(
        "senha/concluido/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete"
    ),
    path('<str:username>', profile, name='users/profile_view.html'),
    path('perfil/<str:username>/', profile, name='profile_view'),
    path('profile/edit', edit_profile, name='edit_profile'),
    
]