from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile, edit_profile, recupera


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', register_view, name='register'),

    path('perfil/<str:username>/', profile, name='profile_view'),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('profile/recupera', recupera, name='recupera'),
]