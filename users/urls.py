from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile, edit_profile, login_view


urlpatterns = [
    path('login/', login_view, name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', register_view, name='register'),

    path('<str:username>', profile, name='users/profile_view.html'),
    path('profile/edit', edit_profile, name='edit_profile'),
    

]