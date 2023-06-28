from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from store.models import Product, OrderItem

# Create your views here.
# * request -> response
# * request handler


# def say_hello(request):
#     return HttpResponse('Hellow world')

def say_hello(request):
    # ? Products: inventory < 10 and price < 20
    # queryset = Product.objects.filter(
    #     unit_price__lt=20, inventory__lt=10)

    # ? Products: inventory < 10 and price is not < 20
    # queryset = Product.objects.filter(
    #     Q(inventory__lt=10) | ~Q(unit_price__lt=20))

    # ? Products: inventory = unit_price     # compare same column in one table
    # queryset = Product.objects.filter(inventory=F('unit_price'))

    # ? Reference to fields of related table
    # queryset = Product.objects.filter(inventory=F('collection__id'))

    # ? Select products that have been ordered and sort them by title

    queryset = Product.objects.filter(
        id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    return render(request, 'hellow.html', {'name': 'Arslan', 'products': list(queryset)})
