from urllib.parse import quote

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from shop.models import Producto, Cart, CartItem

ITEMS_PER_PAGE = 10


def catalogo(request):
    """Listado paginado de todos los productos disponibles."""
    productos = Producto.objects.prefetch_related('imagenes').order_by('id')
    paginator = Paginator(productos, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/catalog.html', {'catalogo': page_obj})


def detalle_producto(request, producto_id):
    """Detalle de un producto individual con carrusel de imágenes."""
    producto = get_object_or_404(
        Producto.objects.prefetch_related('imagenes'),
        id=producto_id
    )
    return render(request, 'home/product_detail.html', {'producto': producto})


@login_required
def add_to_cart(request, producto_id):
    """Agrega un producto al carrito del usuario autenticado."""
    producto = get_object_or_404(Producto, id=producto_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, producto=producto)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'{producto.nombre} agregado al carrito.')
    return redirect('detalle_producto', producto_id=producto_id)


@login_required
def view_cart(request):
    """Muestra el carrito con resumen y enlace de pedido por WhatsApp."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('producto').all()
    total = cart.total

    lines = ['Hola, quiero comprar:']
    for item in items:
        lines.append(f'- {item.quantity} x {item.producto.nombre} (₡{item.subtotal})')
    lines.append(f'Total: ₡{total}')

    whatsapp_text = quote('\n'.join(lines))
    whatsapp_url = f'https://wa.me/?text={whatsapp_text}'

    context = {
        'cart': cart,
        'items': items,
        'total': total,
        'whatsapp_url': whatsapp_url,
    }
    return render(request, 'home/cart.html', context)


@login_required
def remove_from_cart(request, item_id):
    """Elimina un producto del carrito del usuario."""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Producto removido del carrito.')
    return redirect('view_cart')