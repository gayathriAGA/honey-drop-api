from rest_framework.permissions import BasePermission


class IsAuthenticatedView(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated


class ManageUsers(IsAuthenticatedView):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == "admin"


class ManageCategories(BasePermission):

    def has_permission(self, request, view):
        if request.user.role != 'admin':
            return super().has_permission(request, view) and request.method in ["GET", "OPTIONS"]

        return super().has_permission(request, view) and request.user.role == "admin"


class ManageLeads(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'office':
            return super().has_permission(request, view) and request.method in ["GET", "OPTIONS"]

        return super().has_permission(request, view) and request.user.role in ["admin", "sales"]


class ManageCustomers(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'office':
            return super().has_permission(request, view) and request.method in ["GET", "OPTIONS"]
        return super().has_permission(request, view) and request.user.role in ["admin", "service", "sales"]


class ManageProducts(BasePermission):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == "admin"
