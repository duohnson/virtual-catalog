from django.db import models
from django.contrib.auth.models import User


class Producto(models.Model):
    """Producto del catálogo con soporte para múltiples imágenes."""

    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    descripcion = models.TextField()
    is_oferta = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

    def __str__(self):
        return self.nombre

    @property
    def primera_imagen(self):
        """Retorna la primera imagen asociada o None."""
        return self.imagenes.first()


class ProductImage(models.Model):
    """Imagen asociada a un producto."""

    producto = models.ForeignKey(
        Producto, related_name='imagenes', on_delete=models.CASCADE
    )
    imagen = models.ImageField(upload_to='productos/')

    class Meta:
        verbose_name = 'Imagen de producto'
        verbose_name_plural = 'Imágenes de productos'

    def __str__(self):
        return f'Imagen de {self.producto.nombre}'


class Cart(models.Model):
    """Carrito de compras vinculado a un usuario registrado."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f'Carrito de {self.user.username}'

    @property
    def total(self):
        """Suma total de todos los ítems del carrito."""
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    """Ítem individual dentro de un carrito."""

    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Ítem del carrito'
        verbose_name_plural = 'Ítems del carrito'

    def __str__(self):
        return f'{self.quantity} x {self.producto.nombre}'

    @property
    def subtotal(self):
        """Precio unitario multiplicado por la cantidad."""
        return self.producto.precio * self.quantity