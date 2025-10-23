from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CategoryViewSet, SubCategoryViewSet,
    ProductViewSet, LeadViewSet, CustomerViewSet, AuthViewSet
)
from rest_framework.routers import DefaultRouter

class NoSlashRouter(DefaultRouter):
    trailing_slash = ''

router = DefaultRouter(trailing_slash=False)
# router = NoSlashRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='user')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]
