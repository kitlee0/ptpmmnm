from rest_framework import serializers
from bson import ObjectId

class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except:
            raise serializers.ValidationError("Invalid ObjectId")
            raise

class CakeSerializer(serializers.Serializer):
    _id = ObjectIdField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    price = serializers.IntegerField()
    image = serializers.CharField(max_length=255)
    category_id = ObjectIdField()
class CategorySerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
class UserSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=15)
class PaymentSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    order_id = serializers.CharField()
    amount = serializers.IntegerField()
    method = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
class OrderItemSerializer(serializers.Serializer):
    cake_id = serializers.CharField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()
class OrderSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    user_id = serializers.CharField()
    total_price = serializers.IntegerField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    items = OrderItemSerializer(many=True)

