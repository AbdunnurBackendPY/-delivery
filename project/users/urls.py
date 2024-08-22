from django.urls import path
from .views import calculate_delivery_cost

urlpatterns = [
    path('api/calculate/', calculate_delivery_cost, name='calculate_delivery_cost'),
]
