from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product


@api_view(["GET"])
def product_list(request):
    cached_products = cache.get("product_list")

    if cached_products is not None:
        print("CACHE HIT")
        return Response(cached_products)

    print("CACHE MISS")

    products = list(
        Product.objects.values("id", "name", "price", "stock")
    )

    cache.set("product_list", products, timeout=60)

    return Response(products)