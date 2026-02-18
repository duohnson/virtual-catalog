from django.shortcuts import render
from tienda.models import Producto


def index(request):
    """Página principal con productos destacados en oferta."""
    ofertas = Producto.objects.prefetch_related('imagenes').filter(is_oferta=True)
    return render(request, 'home/index.html', {'ofertas': ofertas})


def contacto(request):
    """Página de contacto e información del negocio."""
    return render(request, 'home/contacto.html')