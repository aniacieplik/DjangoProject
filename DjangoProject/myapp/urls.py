from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView

urlpatterns = [
    # API URL patterns (comment these out if needed)
    # path('api/', include(router.urls)),

    # MVT URL patterns for product views
    path('user/products/', ProductListView.as_view(), name='product_list'),
    path('user/products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('user/products/new/', ProductCreateView.as_view(), name='product_create'),
]