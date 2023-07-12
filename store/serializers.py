from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal
# * serializers converts a model instance into a dictionary


class CollectionSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title', 'description', 'slug', 'inventory','unit_price', 'price_with_tax','collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    
    # ? 1: return collection id
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )

    # ? 2: return title of collections
    # collection = serializers.StringRelatedField()

    # ? 3: return both id and title
    # collection = CollectionSerializer()

    # ? 4: another way to serialize an object of collection in product field
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(), 
    #     view_name='collection-detail'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    # * object level validation
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('passwords do not matach')
    #     return data

    # * custom object creation (overiting create method)
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other  = 1  #* modify special field  
    #     product.save()
    #     return product

    # * customer object updation (overwriting update method)
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance