from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend




from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend


from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer,CategorySerializer, ManagersSerializer, CartSerializer, OrderSerializer
from .permissions import IsManager, IsCustomer, IsDeliveryCrew


GROUP_NAMES = {'manager':"Manager", "delivery-crew":"Delivery crew"}

    

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    PageNumberPagination.page_size_query_param = 'page_size'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # Add OrderingFilter
    ordering_fields = ['price']  # Specify fields by which items can be sorted


    def get_permissions(self):
        if self.request.method in ['POST', 'PUT','PATCH','DELETE']:
            return [IsManager()]

        else: return [IsAuthenticated()]

    def get_queryset(self) :
        category = self.request.query_params.get('category')

        if category:
            queryset = MenuItem.objects.filter(category__title=category)
        else:
            queryset = MenuItem.objects.all()
        
        return queryset
        

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT','PATCH']:
            return [IsManager()]

        else: return [IsAuthenticated()]


class CartView(viewsets.ViewSet):
    permission_classes = [IsCustomer]
    def list(self, request):
        items_objects  = Cart.objects.filter(user = request.user)
        items = CartSerializer(items_objects,many=True)
        return Response(items.data)
    
    def create(self, request):
        menuitem_id = request.data.get('menuitem_id')
        menuitem = MenuItem.objects.get(id = menuitem_id)
        try:
            cart_item = Cart.objects.get(user=request.user, menuitem = menuitem)
            cart_item.quantity += 1
            cart_item.price += cart_item.unit_price
            cart_item.save()
            return Response({"massage": f'{cart_item} added'})

        except ObjectDoesNotExist:
            item_to_cart = Cart(user = request.user, menuitem=menuitem, quantity = 1, unit_price = menuitem.price, price = menuitem.price)
            item_to_cart.save()
            return Response({'massage': "added to cart"})

    def destroy(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({"massage":"the cart is empty now"})




class GroupViewSet(viewsets.ViewSet):
    permission_classes = [IsManager]

    def list(self, request, url_group_name):
        # verify this is a valid group
        try:
            group_name = GROUP_NAMES[url_group_name]
        except KeyError:
            return Response(status.HTTP_404_NOT_FOUND)

        group = Group.objects.get(name=group_name)
        users = User.objects.filter(groups__in=[group])
        items = ManagersSerializer(users, many=True)
        return Response(items.data)

    def create(self, request, url_group_name):
        # verify this is a valid group
        try:
            group_name = GROUP_NAMES[url_group_name]
        except KeyError:
            return Response(status.HTTP_404_NOT_FOUND)
        
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        group = Group.objects.get(name=group_name)
        group.user_set.add(user)
        return Response({"message": f"user added to the {group_name} group"}, status.HTTP_201_CREATED)

    def destroy(self, request, url_group_name, pk):
        try:
            group_name = GROUP_NAMES[url_group_name]
        except KeyError:
            return Response(status.HTTP_404_NOT_FOUND)
        
        user = get_object_or_404(User, id=pk)
        manager_group = Group.objects.get(name=group_name)
        manager_group.user_set.remove(user)
        return Response({"message": f"user removed from the {group_name} group"}, status.HTTP_200_OK)


def _is_user_in_group(user,group_name):
        if group_name=="Customer":
            return not user.groups.all().exists()
        else:
            group = Group.objects.get(name=group_name)
            return group in user.groups.all()

class OrderViewSet(viewsets.ViewSet):
    
    permission_classes=[IsAuthenticated]

    
    def list(self,request):
        if _is_user_in_group(request.user,'Customer'):
            order_items = Order.objects.filter(user=request.user)
        
        elif _is_user_in_group(request.user,'Manager'):
            order_items = Order.objects.all()
            
        
        elif _is_user_in_group(request.user, 'Delivery crew'):
            order_items = Order.objects.filter(delivery_crew = request.user)

        
        else:
            return Response({"massage":"you are not authenticated"}, status.HTTP_403_FORBIDDEN)
        
        items = OrderSerializer(order_items, many=True)
        return Response(items.data)
    
    def create(self, request):
        # get all the items in the cart
        cart_menuitems = Cart.objects.filter(user=request.user)
        # create new order
        new_order = Order(user=request.user,total =0,date=timezone.now())
        new_order.save()
        for item in cart_menuitems:
            orderitem = OrderItem(order=new_order, menuitem=item.menuitem, quantity = item.quantity, unit_price = item.unit_price, price=item.price)
            new_order.total+=item.price
            orderitem.save()
            new_order.save()
        # empty user cart
        Cart.objects.filter(user=request.user).delete()
        return Response({"massage":"order created"})

        
class SingleOrderViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['update','destroy']:
            permission_classes = [IsManager]
        elif self.action == 'partial_update':
             permission_classes =[IsManager | IsDeliveryCrew]
        else:
            permission_classes=[IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, pk):
        try:
            order_obj = Order.objects.get(id=pk, user = request.user)
            order = OrderSerializer(order_obj)
            return Response(order.data) 
        except ObjectDoesNotExist:
            return Response({"massage":"you are not authenticated"},status.HTTP_403_FORBIDDEN)
    
    def update(self, request, pk):
        """
        Note: According to my understanding, the Put method here is supposed to actually replace the existing order,
          so all the necessary fields are required to create a new order, only the order id remains. In my opinion,
            a put option is unnecessary here.
        """

        order = get_object_or_404(Order, id=pk)

        user_id = request.data.get('user_id')
        total = request.data.get('total')
        date = request.data.get('date')
        if user_id and total and date:
            try:
                user = User.objects.get(id=user_id)
                if not _is_user_in_group(user, "Customer"):
                    raise ObjectDoesNotExist
            except ObjectDoesNotExist:
                return Response({"massage":"invlaid user"}, status.HTTP_400_BAD_REQUEST)
            
            order.user = user
            order.total = total
            order.date = date

        else:
            return Response({"massage":"You have entered all required fields"}, status.HTTP_400_BAD_REQUEST)
        
        delivery_crew_name = request.data.get('delivery_crew_name')
        if delivery_crew_name:
            try:
                delivery_crew = User.objects.get(username=delivery_crew_name)
            except ObjectDoesNotExist:
                return Response({"massage":"there is not such delivery crew"}, status.HTTP_400_BAD_REQUEST)
            
            # case of the username is a valid user, now check if he in delivery crew
            if _is_user_in_group(delivery_crew, "Delivery crew"):
                order.delivery_crew = delivery_crew
            else:
                return Response({"massage":"there is not such delivery crew"}, status.HTTP_400_BAD_REQUEST)


        status_value = request.data.get('status')
        if status_value:
            order.status = status_value
        

        order.save()
        return Response({"massage": "updated"})

    def partial_update(self, request, pk):
        order_status = request.data.get('status')
        delivery_crew_name = request.data.get('delivery_crew_name')
        order = get_object_or_404(Order,id=pk)
        
        if order_status and order.delivery_crew == request.user:
            order.status=order_status
        elif order_status and not order.delivery_crew == request.user:
            return Response({"massage":"delivery crew can only access their orders"}, status.HTTP_403_FORBIDDEN)

        if delivery_crew_name and _is_user_in_group(request.user, 'Manager'):
            delivery_crew = User.objects.get(username=delivery_crew_name)
            order.delivery_crew = delivery_crew
        elif delivery_crew_name and not _is_user_in_group(request.user, 'Manager'):
            return Response({"massage":"you are not allowed to change the delivery crew"}, status.HTTP_400_BAD_REQUEST)
        
        order.save()
        return Response({"massage":"updated"})
    
    def destroy(self, request, pk):
        order = get_object_or_404(Order, id = pk)
        order.delete()
        return Response({"massage":f"order {pk} deleted"})
        






        
