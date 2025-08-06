from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, CartItem, Wishlist, WishlistItem, Order, OrderItem
import json
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm

class BaseView:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) if hasattr(super(), 'get_context_data') else {}
        context['categories'] = Category.objects.all().order_by('name')
        
        # Add cart count to context
        cart_count = 0
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=self.request.user)
                cart_count = cart.total_items
            except Cart.DoesNotExist:
                pass
        else:
            session_key = self.request.session.session_key
            if session_key:
                try:
                    cart = Cart.objects.get(session_key=session_key)
                    cart_count = cart.total_items
                except Cart.DoesNotExist:
                    pass
        
        context['cart_count'] = cart_count
        return context

class HomeView(BaseView, ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'featured_products'
    
    def get_queryset(self):
        return Product.objects.filter(featured=True, available=True)[:6]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_arrivals'] = Product.objects.filter(available=True).order_by('-created_at')[:4]
        return context

class ProductListView(BaseView, ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        return Product.objects.filter(available=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = Product.objects.filter(available=True).count()
        return context

class CategoryProductsView(BaseView, ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        try:
            self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
            return Product.objects.filter(category=self.category, available=True)
        except Http404:
            print(f"Category not found: {self.kwargs['slug']}")
            print(f"Available categories: {list(Category.objects.values_list('slug', flat=True))}")
            raise
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        context['total_products'] = Product.objects.filter(available=True).count()
        return context

class ProductDetailView(BaseView, DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.filter(available=True)

def about_view(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'store/about.html', {'categories': categories})

def contact_view(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'store/contact.html', {'categories': categories})

def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def get_or_create_wishlist(request):
    """Get or create wishlist for user or session"""
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        wishlist, created = Wishlist.objects.get_or_create(session_key=request.session.session_key)
    return wishlist

@require_POST
@login_required
def add_to_cart(request):
    """Add product to cart via AJAX"""
    try:
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            size = data.get('size', '')
        else:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
            size = request.POST.get('size', '')
        
        if not product_id:
            return JsonResponse({
                'success': False,
                'message': 'Product ID is required'
            })
        
        product = get_object_or_404(Product, id=product_id, available=True)
        cart = get_or_create_cart(request)
        
        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'cart_count': cart.total_items,
            'cart_total': float(cart.total_price)
        })
        
    except Exception as e:
        print(f"Error adding to cart: {e}")  # Debug logging
        return JsonResponse({
            'success': False,
            'message': 'Error adding item to cart. Please try again.'
        })

@require_POST
def add_to_wishlist(request):
    """Add product to wishlist via AJAX"""
    try:
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            product_id = data.get('product_id')
        else:
            product_id = request.POST.get('product_id')
        
        if not product_id:
            return JsonResponse({
                'success': False,
                'message': 'Product ID is required'
            })
        
        product = get_object_or_404(Product, id=product_id, available=True)
        wishlist = get_or_create_wishlist(request)
        
        # Check if item already exists in wishlist
        wishlist_item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            product=product
        )
        
        if created:
            return JsonResponse({
                'success': True,
                'message': f'{product.name} added to wishlist!',
                'action': 'added'
            })
        else:
            # Remove from wishlist if already exists
            wishlist_item.delete()
            return JsonResponse({
                'success': True,
                'message': f'{product.name} removed from wishlist!',
                'action': 'removed'
            })
        
    except Exception as e:
        print(f"Error updating wishlist: {e}")  # Debug logging
        return JsonResponse({
            'success': False,
            'message': 'Error updating wishlist. Please try again.'
        })

def cart_view(request):
    """Display cart contents"""
    cart = get_or_create_cart(request)
    categories = Category.objects.all().order_by('name')
    
    context = {
        'cart': cart,
        'categories': categories,
        'cart_count': cart.total_items
    }
    return render(request, 'store/cart.html', context)

@require_POST
def update_cart_item(request):
    """Update cart item quantity via AJAX"""
    try:
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = int(data.get('quantity', 1))
        else:
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 1))
        
        if not item_id:
            return JsonResponse({
                'success': False,
                'message': 'Item ID is required'
            })
        
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'cart_total': float(cart.total_price),
            'item_total': float(cart_item.get_total_price()) if quantity > 0 else 0
        })
        
    except Exception as e:
        print(f"Error updating cart item: {e}")  # Debug logging
        return JsonResponse({
            'success': False,
            'message': 'Error updating cart. Please try again.'
        })

@require_POST
def remove_from_cart(request):
    """Remove item from cart via AJAX"""
    try:
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            item_id = data.get('item_id')
        else:
            item_id = request.POST.get('item_id')
        
        if not item_id:
            return JsonResponse({
                'success': False,
                'message': 'Item ID is required'
            })
        
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_count': cart.total_items,
            'cart_total': float(cart.total_price)
        })
        
    except CartItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Item not found in cart'
        })
    except Exception as e:
        print(f"Error removing item from cart: {e}")  # Debug logging
        return JsonResponse({
            'success': False,
            'message': 'Error removing item from cart. Please try again.'
        })

def wishlist_view(request):
    """Display wishlist contents"""
    wishlist = get_or_create_wishlist(request)
    categories = Category.objects.all().order_by('name')
    
    context = {
        'wishlist': wishlist,
        'categories': categories,
        'cart_count': get_or_create_cart(request).total_items
    }
    return render(request, 'store/wishlist.html', context)


def checkout_view(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('store:cart_view')
    if request.method == 'POST':
        # Collect form data
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        # Save order summary in session (for demo)
        request.session['order_summary'] = {
            'full_name': full_name,
            'address': address,
            'city': city,
            'postal_code': postal_code,
            'phone': phone,
            'payment_method': payment_method,
            'items': [
                {
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'size': item.size,
                    'total': float(item.get_total_price())
                } for item in cart.items.all()
            ],
            'total_price': float(cart.total_price)
        }
        # Clear cart
        cart.items.all().delete()
        return redirect(reverse('store:order_success'))
    return render(request, 'store/checkout.html', {'cart': cart})

def order_success(request):
    order_summary = request.session.get('order_summary')
    if not order_summary:
        return redirect('store:product_list')
    return render(request, 'store/order_success.html', {'order': order_summary})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('store:login')  # 👈 Redirect back to login page
    else:
        login_form = AuthenticationForm()
        register_form = UserRegistrationForm()

    context = {
        'login_form': login_form,
        'register_form': register_form,
    }
    return redirect('store:home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    register_form = UserRegistrationForm(request.POST or None)
    login_form = AuthenticationForm()

    if request.method == 'POST':
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, "Please fix the errors in the form.")  # ✅ Show error popup

    context = {'register_form': register_form, 'login_form': login_form}
    return render(request, 'base.html', context)


def logout_view(request):
    logout(request)
    return redirect('store:home')

@login_required
def profile_view(request):
    user = request.user
    orders = user.orders.all().order_by('-created_at')
    return render(request, 'store/profile.html', {'user': user, 'orders': orders})


def checkout_view(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('store:cart_view')
    if request.method == 'POST':
        # Collect form data
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        # Save order to DB
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            postal_code=postal_code,
            phone=phone,
            payment_method=payment_method,
            total_price=cart.total_price
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                size=item.size,
                total=item.get_total_price()
            )
        # Save order summary in session (optional, for order_success page)
        request.session['order_summary'] = {
            'order_id': order.id,
            'full_name': full_name,
            'address': address,
            'city': city,
            'postal_code': postal_code,
            'phone': phone,
            'payment_method': payment_method,
            'items': [
                {
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'size': item.size,
                    'total': float(item.get_total_price())
                } for item in cart.items.all()
            ],
            'total_price': float(cart.total_price)
        }
        # Clear cart
        cart.items.all().delete()
        return redirect(reverse('store:order_success'))
    return render(request, 'store/checkout.html', {'cart': cart})


