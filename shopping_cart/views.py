from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Profile
from products.models import Product

from shopping_cart.extras import generate_order_id, transact, generate_client_token
from shopping_cart.models import OrderItem, Order, Transaction

import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_user_pending_order(request):
    # Para obtener la orden del usario
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # obtener el único pedido en la lista de pedidos filtrados
        return order[0]
    return 0


@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # comprobar si el usuario ya posee este producto
    if product in request.user.profile.ebooks.all():
        messages.info(request, 'Ya tienes este producto')
        return redirect(reverse('products:product-list')) 
    #  crear artículo de pedido del producto seleccionado
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # Crear orden asociado con el usuario
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generar un código de referencia
        user_order.ref_code = generate_order_id()
        user_order.save()

    # mostrar mensaje de confirmación y redirigir de nuevo a la misma página
    messages.info(request, "item added to cart")
    return redirect(reverse('products:product-list'))


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('shopping_cart:order_summary'))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'shopping_cart/order_summary.html', context)


@login_required()
def checkout(request, **kwargs):
    client_token = generate_client_token()
    existing_order = get_user_pending_order(request)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=100*existing_order.get_cart_total(),
                    currency='usd',
                    description='Example charge',
                    source=token,
                )

                return redirect(reverse('shopping_cart:update_records',
                        kwargs={
                            'token': token
                        })
                    )
            except stripe.CardError as e:
                message.info(request, "Your card has been declined.")
        else:
            result = transact({
                'amount': existing_order.get_cart_total(),
                'payment_method_nonce': request.POST['payment_method_nonce'],
                'options': {
                    "submit_for_settlement": True
                }
            })

            if result.is_success or result.transaction:
                return redirect(reverse('shopping_cart:update_records',
                        kwargs={
                            'token': result.transaction.id
                        })
                    )
            else:
                for x in result.errors.deep_errors:
                    messages.info(request, x)
                return redirect(reverse('shopping_cart:checkout'))
            
    context = {
        'order': existing_order,
        'client_token': client_token,
        'STRIPE_PUBLISHABLE_KEY': publishKey
    }

    return render(request, 'shopping_cart/checkout.html', context)


@login_required()
def update_transaction_records(request, token):
    # hacer que se procese el pedido
    order_to_purchase = get_user_pending_order(request)

    # actualizar el pedido realizado
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    
    # obtener todos los artículos en el pedido: genera un conjunto de consultas
    order_items = order_to_purchase.items.all()

    # actualizar artículos de pedido
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Agregar productos al perfil de usuario
    user_profile = get_object_or_404(Profile, user=request.user)
    # obtener los productos de los artículos
    order_products = [item.product for item in order_items]
    user_profile.ebooks.add(*order_products)
    user_profile.save()

    
    # crear una transacción
    transaction = Transaction(profile=request.user.profile,
                            token=token,
                            order_id=order_to_purchase.id,
                            amount=order_to_purchase.get_cart_total(),
                            success=True)
    # guarda la transacción (de lo contrario, no existe)
    transaction.save()


    # Enviar un correo electrónico al cliente
    
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('accounts:my_profile'))


def success(request, **kwargs):
    # Mensaje que indica que la transacción fue exitosa
    return render(request, 'shopping_cart/purchase_success.html', {})
