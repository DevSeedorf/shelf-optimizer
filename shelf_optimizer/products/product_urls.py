from django.urls import path
from .views import product_list, add_product, optimize_shelves, shelf_allocation, delete_product, optimization_history, clear_optimization_history

urlpatterns = [
    path('', product_list, name='product_list'),
    path('add/', add_product, name='add_product'),
    path('optimize/', optimize_shelves, name='optimize_shelves'),
    path('allocation/', shelf_allocation, name='shelf_allocation'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
    path('results/', optimization_history, name='optimization_history'),
    path('results/clear/', clear_optimization_history, name='clear_optimization_history'),
]
