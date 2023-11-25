from django.urls import path, include
from . import views 
  
urlpatterns = [ 
    path('', include('djoser.urls')), 
    path('', include('djoser.urls.authtoken')), 
    path('categories', views.CategoriesView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('groups/<str:url_group_name>/users', views.GroupViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('groups/<str:url_group_name>/users/<int:pk>', views.GroupViewSet.as_view({'delete':'destroy'})),
    path('cart/menu-items', views.CartView.as_view({'get': 'list', 'post':'create','delete':'destroy'})),
    path('orders', views.OrderViewSet.as_view({'get':'list', 'post':'create'})),
    path('orders/<int:pk>',views.SingleOrderViewSet.as_view({'get':'retrieve', 'put': 'update', 'patch':'partial_update', 'delete':'destroy'})),

] 