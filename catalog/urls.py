from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import HomeListView, ContactTemplateView, ProductDetailView
from django.conf import settings
from django.conf.urls.static import static

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeListView.as_view(), name="catalog_list"),
    path("contacts/", ContactTemplateView.as_view(), name="contacts"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="catalog_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
