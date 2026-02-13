from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product, Variation
from .models import Cart, CartItems, CheckoutDB
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse


def merge_carts(user, session_key):
    """
    Merges anonymous user's cart items with authenticated user's cart items.
    
    Process:
    Get the anonymous cart by session key
    Get the user's authenticated cart (or create one)
    For each item in the anonymous cart:
    Check if the user already has the same product with same variations
    If yes: sum the quantities
    If no: transfer the item to the user's cart
    Optionally delete the anonymous cart after merging
    
    Args:
        user: The authenticated user object
        session_key: The session key of the anonymous user
    """
    try:
        # Get the anonymous cart by session key
        anonymous_cart = Cart.objects.get(cart_id=session_key)
    except Cart.DoesNotExist:
        # No anonymous cart to merge
        return
    
    # Get or create the user's authenticated cart using the new session key
    try:
        user_cart = Cart.objects.get(cart_id=session_key)
    except Cart.DoesNotExist:
        user_cart = Cart.objects.create(cart_id=session_key)
    
    # Get all items from the anonymous cart
    anonymous_cart_items = CartItems.objects.filter(cart=anonymous_cart)
    
    for anon_item in anonymous_cart_items:
        # Get the variations for this anonymous item
        anon_variations = list(anon_item.variations.all())
        
        # Check if user already has this product with the same variations
        user_cart_items = CartItems.objects.filter(
            user=user,
            product=anon_item.product
        )
        
        item_found = False
        
        for user_item in user_cart_items:
            user_variations = list(user_item.variations.all())
            
            # Compare variations: both list must have same elements
            if set(anon_variations) == set(user_variations):
                # Same product with same variations - merge quantities
                user_item.quantity += anon_item.quantity
                user_item.save()
                item_found = True
                break
        
        if not item_found:
            anon_item.user = user
            anon_item.cart = user_cart
            anon_item.save()
    
    
    if anonymous_cart.cart_id != user_cart.cart_id:
        anonymous_cart.delete()

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) 
    
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
    
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exists = CartItems.objects.filter(product=product, user=current_user, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItems.objects.filter(product=product, user=current_user, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItems.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItems.objects.create(product=product, quantity=1, user=current_user, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItems.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItems.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItems.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItems.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItems.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItems.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItems.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItems.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItems.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItems.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        
        delivery = request.GET.get('delivery')

        if delivery:
            request.session['delivery'] = delivery
        else:
            delivery = request.session.get('delivery')

       
        if delivery == 'dhaka':
            tax = 70
        elif delivery == 'suburbs':
            tax = 100
        elif delivery == 'outside':
            tax = 130
        else:
            tax = 0

        if request.user.is_authenticated:
            cart_items = CartItems.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItems.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.product.product_price * cart_item.quantity
            quantity += cart_item.quantity

        grand_total = total + tax

        
        if request.user.is_authenticated and delivery:
            CheckoutDB.objects.update_or_create(
                user=request.user,
                defaults={
                    'total_amount': grand_total,
                    'delivery_area': delivery,
                }
            )

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'delivery': delivery,
    }
    return render(request, 'store/cart.html', context)



@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):

    
    delivery = request.session.get('delivery')
    if not delivery:
        return redirect('cart')

    
    delivery_charge_map = {
        'dhaka': 70,
        'suburbs': 100,
        'outside': 130,
    }

    delivery_charge = delivery_charge_map.get(delivery, 0)

    try:
        if request.user.is_authenticated:
            cart_items = CartItems.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItems.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.product.product_price * cart_item.quantity
            quantity += cart_item.quantity

        grand_total = total + delivery_charge

        
        checkout_data = CheckoutDB.objects.filter(user=request.user).last()

    except ObjectDoesNotExist:
        cart_items = []
        checkout_data = None
        grand_total = 0

    context = {
        'cart_items': cart_items,
        'total': total,
        'delivery_area': delivery,
        'delivery_charge': delivery_charge,
        'grand_total': grand_total,
        'checkout_data': checkout_data,
    }

    return render(request, 'store/checkout.html', context)
