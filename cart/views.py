from django.shortcuts import render,get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse,HttpResponse
from django.contrib import messages

# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods

    quantities = cart.get_quants
    
    totals = cart.cart_total()
    
    return render(request,"cart_summary.html",{"cart_products":cart_products,"quantities":quantities,"totals":totals})
    
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        
        
        cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()


        # response = JsonResponse({'Product Name:': product.name })
        response = JsonResponse({'qty': cart_quantity})

        messages.success(request, ("Product Added to Cart......"))


        return response
    return HttpResponse("Invalid request", status=400)
        
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        
        response = JsonResponse({'product': product_id})
        messages.success(request, ("Item deleted for the shoping cart"))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Call the update method on the cart
        cart.update(product=product_id, quantity=product_qty)

        # Return JSON response for the updated quantity
        response = JsonResponse({'qty': product_qty})
        messages.success(request, ("Your Cart has been Update......"))
        return response