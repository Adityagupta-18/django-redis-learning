from django.urls import path
from .views import product_list, rate_limit_test

urlpatterns = [
    path("products/", product_list, name="product-list"),
    path("rate-limit-test/", rate_limit_test, name="rate-limit-test"),
]