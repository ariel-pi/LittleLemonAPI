from rest_framework import serializers 
from rest_framework.validators import UniqueTogetherValidator 
from django.contrib.auth.models import User
  
from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category','category_id']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['menuitem','quantity','unit_price','price']


class ManagersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'username']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    # Add a field for menu items
    menuitems = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id','user', 'delivery_crew', 'status', 'total', 'date', 'menuitems']

    def get_menuitems(self, obj):
        # Retrieve and format the related menu items for the order
        order_items = OrderItem.objects.filter(order=obj)
        serialized_menu_items = OrderItemSerializer(order_items, many=True).data
        return serialized_menu_items