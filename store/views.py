from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        querySet = Product.objects.select_related('collection').all()
        # many -> query set iterate over each set
        serializer = ProductSerializer(querySet, many=True, context = {'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)   #! deserialization
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response("serializer.validated_data")
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # ? same result as before but less code
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        # if product.orderitem_set.count() > 0:
        if product.orderitems.count() > 0:
            return Response({'error', 'product cannot be deleted because it is associated with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({'message': 'Success'},status=status.HTTP_204_NO_CONTENT)


@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)
