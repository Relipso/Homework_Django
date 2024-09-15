from django.core.cache import cache
from catalog.models import Category, Product


def get_categories():
    cache_key = 'categories_list'
    cache_time = 60 * 1
    categories = cache.get(cache_key)
    if not categories:
        categories = Category.objects.all()
        cache.set(cache_key, categories, cache_time)
    return categories


def get_products():
    cache_key = 'products_list'
    cache_time = 60 * 1
    products = cache.get(cache_key)
    if not products:
        products = Product.objects.all()
        cache.set(cache_key, products, cache_time)
    return products
