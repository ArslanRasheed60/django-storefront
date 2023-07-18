from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product, Collection, OrderItem
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models import Count

#** Collectio View SEts
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error', 'product cannot be deleted because it is associated with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     # if product.orderitem_set.count() > 0:
    #     if product.orderitems.count() > 0:
    #         return Response({'error', 'product cannot be deleted because it is associated with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response({'message': 'Success'},status=status.HTTP_204_NO_CONTENT)


#* converting class view to generic api view
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

# #* class view to handle api requests
# class ProductList(APIView):
#     def get(self, request):
#         querySet = Product.objects.select_related('collection').all()
#         # many -> query set iterate over each set
#         serializer = ProductSerializer(querySet, many=True, context = {'request': request})
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)   #! deserialization
#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response("serializer.validated_data")
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # ? same result as before but less code
#         serializer.is_valid(raise_exception=True)
#         # serializer.validated_data
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)  

#* functions view to handle api requests
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         pass
#     elif request.method == 'POST':
#         pass

#* customizing generic serializer
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        # if product.orderitem_set.count() > 0:
        if product.orderitems.count() > 0:
            return Response({'error', 'product cannot be deleted because it is associated with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({'message': 'Success'},status=status.HTTP_204_NO_CONTENT)

# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         # if product.orderitem_set.count() > 0:
#         if product.orderitems.count() > 0:
#             return Response({'error', 'product cannot be deleted because it is associated with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response({'message': 'Success'},status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
        
#     elif request.method == 'PUT':
        
#     elif request.method == 'DELETE':
        

#** Collection view set
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error', 'collection cannot be deleted because it is associated with product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error', 'collection cannot be deleted because it is associated with product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response({'message': 'Success'},status=status.HTTP_204_NO_CONTENT)

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer



# class CollectionList(APIView):
#     def get(self, request):
#         querySet = Collection.objects.annotate(products_count=Count('products')).all().order_by('id')
#         serializer = CollectionSerializer(querySet, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = CollectionSerializer(data=request.data) #! de-serialization
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)    


#* class generic view customizable
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({'error', 'collection cannot be deleted because it is associated with product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response({'message': 'Success'},status=status.HTTP_204_NO_CONTENT)

# class CollectionDetail(APIView):
#     def get(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error', 'collection cannot be deleted because it is associated with product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response({'message': 'Success'},status=status.HTTP_204_NO_CONTENT)
