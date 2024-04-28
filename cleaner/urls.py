from django.urls import path
from .import views
from.views import AddComment


app_name = 'cleaner'

urlpatterns = [
    path('',views.ProductListView.as_view(), name='index'),
    path('category/<int:pk>/',views.CategoryProductsList.as_view(), name='category'),
    path('product_detail/<int:pk>/',views.ProductDetailView.as_view(), name='product_detail'),

    path('cart_summary/',views.cart_summary, name='cart_summary'),
    path('cart_add/',views.cart_add, name='cart_add'),
    path('cart_delete/',views.cart_delete, name='cart_delete'),
    path('cart_update/',views.cart_update, name='cart_update'),
    path('order_view/',views.OrderView.as_view(), name='order'),
    path('get_orders/',views.GetOrdersView.as_view(), name='get_orders'),
    path('add-comment/<int:id>', AddComment.as_view(), name='add_comment'),
]
