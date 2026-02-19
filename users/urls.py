from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registro_view, name='register'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.perfil_view, name='profile'),
    path('perfil/', views.perfil_view, name='perfil'),
]