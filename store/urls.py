from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('cart',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem,name="update-item"),
    path('registration/',views.registeration,name="registration"),
    path('login/',views.store_login,name="login"),
    path('logout/',views.log_out,name="logout"),
]