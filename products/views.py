from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from django.http import JsonResponse
import redis
from django.conf import settings

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


redis_client = redis.Redis.from_url(
settings.REDIS_URL,
decode_responses=True,
)

def rate_limit_test(request):
    ip_address = request.META.get("REMOTE_ADDR", "unknown")
    key = f"rate_limit:test:{ip_address}"

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, 60)

    if count > 5:
        return JsonResponse(
            {"error": "Too many requests. Try again later."},
            status=429,
            headers={"Retry-After": str(redis_client.ttl(key))},
        )

    return JsonResponse({
        "message": "Request allowed",
        "requests_used": count,
        "limit": 5,
    })