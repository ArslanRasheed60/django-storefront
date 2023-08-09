from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem
from decimal import Decimal
# * serializers converts a model instance into a dictionary


class CollectionSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


    # product_count = serializers.SerializerMethodField(method_name='calculate_products_count')

    # def calculate_products_count(self, collection: Collection):
    #     return collection.product_set.count()



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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name' ,'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price
        

    class Meta:
        model = CartItem
        fields = ['id','product','quantity', 'total_price']    

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No Product wwith given id was found")
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            #* updating an item
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            #* creating an item
            self.instance = CartItem.objects.create(cart_id = cart_id, **self.validated_data)
        
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']