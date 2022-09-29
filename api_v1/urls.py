from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api_v1 import views
from api_v1.views import OrdersView

app_name = 'api_v1'
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('order_products', views.OrderProductsView)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrdersView.as_view(), name='orders_view'),
    path('orders/<int:pk>/', OrdersView.as_view(), name='orders_view'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
]
