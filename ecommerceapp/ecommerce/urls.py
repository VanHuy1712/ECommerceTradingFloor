from django.urls import path, include, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('products', views.ProductViewSet, basename='products')
router.register('shops', views.ShopViewSet, basename='shops')
router.register('comments', views.CommentViewSet, basename='comments')
router.register('payments', views.PaymentsViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
]

