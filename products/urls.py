from django.urls import path
from .views import product_list, rate_limit_test, drf_throttle_test

urlpatterns = [
    path("products/", product_list, name="product-list"),
    path("rate-limit-test/", rate_limit_test, name="rate-limit-test"),
    path(
    "drf-throttle-test/",
    drf_throttle_test,
    name="drf-throttle-test",
),
]