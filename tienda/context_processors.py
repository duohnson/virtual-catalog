from tienda.models import Cart


def cart_count(request):
    """Inyecta la cantidad de ítems del carrito en el contexto global."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return {'cart_count': cart.items.count()}
    return {'cart_count': 0}