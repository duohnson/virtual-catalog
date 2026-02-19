from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Perfil extendido del usuario con foto de perfil."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'Perfil de {self.user.username}'
