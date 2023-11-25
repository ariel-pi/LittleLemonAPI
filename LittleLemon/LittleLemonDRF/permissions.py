from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and belongs to the "Manager" group
        return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and not belongs to any group
        return request.user.is_authenticated and (not request.user.groups.all().exists())

class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and belongs to the "Manager" group
        return request.user.is_authenticated and request.user.groups.filter(name='Delivery crew').exists()
