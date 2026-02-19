from django.db import models

class EmojiEffectConfig(models.Model):
	emoji = models.CharField(max_length=8, default='❄️', help_text='Emoji para el efecto decorativo')
	opacity = models.FloatField(default=1.0, help_text='Opacidad del emoji (0.0 a 1.0)')

	class Meta:
		verbose_name = 'Configuración de efecto emoji'
		verbose_name_plural = 'Configuraciones de efecto emoji'

	def __str__(self):
		return f"Emoji: {self.emoji} | Opacidad: {self.opacity}"
