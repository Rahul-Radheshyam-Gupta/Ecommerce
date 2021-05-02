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
    path('admin_dashboard/',views.AdminDashboard.as_view(),name="admin-dashboard"),
    path('product/<int:id>/',views.product_detail,name="product-detail"),
    path('product_feature/',views.product_detail_add,name="product-feature"),
    path('feature/<int:id>/',views.product_feature_delete,name="feature-delete"),
]