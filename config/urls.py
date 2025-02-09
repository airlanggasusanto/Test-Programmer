from django.contrib import admin
from django.urls import path
from core.views import index, add_product, delete_product, get_product, update_product

urlpatterns = [
    path('', index, name='index'),
    path('add_product/', add_product, name='add_product'),
    path('get_product/<int:product_id>/', get_product, name='get_product'),
    path("delete_product/", delete_product, name="delete_product"),
    path("update_product/", update_product, name="update_product"),
]
