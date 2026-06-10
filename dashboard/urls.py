from django.urls import path
from dashboard.views import dashboard, historico_dashboard_view

urlpatterns = [
    path('', dashboard , name='dashboard'),
    path('historico/', historico_dashboard_view, name='historico_dashboard')
]
