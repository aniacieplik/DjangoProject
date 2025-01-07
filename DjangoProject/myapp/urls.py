from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

router = DefaultRouter()
router.register(r'user/products', ProductViewSet, basename='product')
urlpatterns = [
    path('api/', include(router.urls)),
]