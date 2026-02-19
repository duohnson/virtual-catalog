from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

from shop.models import Producto

ITEMS_PER_PAGE = 10


def buscar(request):
    """Busca productos por nombre o descripción con paginación."""
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(
        Q(nombre__icontains=query) | Q(descripcion__icontains=query)
    ).prefetch_related('imagenes').order_by('id')

    paginator = Paginator(productos, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/search.html', {
        'query': query,
        'catalogo': page_obj,
    })