from django.urls import path
from catalog.apps import CatalogConfig
from . import views
from catalog.views import ProductListView, ContactsPageView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CategoryListView
from django.views.decorators.cache import cache_page  # Импортируем cache_page

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", cache_page(60 * 1)(ProductDetailView.as_view()), name="products_detail"),
    path("contacts/", ContactsPageView.as_view(), name="contacts"),
    path('create/', ProductCreateView.as_view(), name="products_create"),
    path('update/<int:pk>', ProductUpdateView.as_view(), name="products_update"),
    path("product_delete/<int:pk>/", ProductDeleteView.as_view(), name="products_delete"),
    path('product/<int:pk>/unpublish/', views.unpublish_product, name='unpublish_product'),
    path('categories/', CategoryListView.as_view(), name='categories_list'),
]
