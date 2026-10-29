from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from django.http import JsonResponse
import redis
from django.conf import settings
from rest_framework.throttling import ScopedRateThrottle



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


RATE_LIMIT_SCRIPT = """
local count = redis.call('INCR', KEYS[1])

if count == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end

return count
"""

def rate_limit_test(request):
    ip_address = request.META.get("REMOTE_ADDR", "unknown")
    key = f"rate_limit:test:{ip_address}"

    count = redis_client.eval(
        RATE_LIMIT_SCRIPT,
        1,
        key,
        60,
    )

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



@api_view(["GET"])
def drf_throttle_test(request):
    return Response({"message": "Request allowed by DRF"})

drf_throttle_test.cls.throttle_classes = [ScopedRateThrottle]
drf_throttle_test.cls.throttle_scope = "test"