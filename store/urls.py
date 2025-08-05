from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:slug>/', views.CategoryProductsView.as_view(), name='category_products'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    
    # Wishlist URLs
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
