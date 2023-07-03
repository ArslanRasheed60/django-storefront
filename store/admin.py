from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

# * another way to register product model
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['title', 'unit_price']
# admin.site.register(models.Product, ProductAdmin)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10

    def orders(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?' + urlencode({
                   'customer__id': str(customer.id)
               }))
        return format_html('<a href={}>{}</a>', url, customer.orders)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            orders=Count('order')
        )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    list_select_related = ['customer']
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    # * rendering anchor link
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # ? reverse('admin:app_model_page')
        url = (reverse('admin:store_product_changelist')
               + '?' +
               urlencode({
                   'collection__id': str(collection.id)
               }))
        return format_html('<a href="{}">{}</a>', url,
                           collection.products_count)

    # * return count
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count=Count('product')

        )
