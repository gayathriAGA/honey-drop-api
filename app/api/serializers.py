from rest_framework import serializers
from .models import User, Category, SubCategory, Product, Lead, Customer, ProductInterests, CustomerProducts
from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import make_password


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'status', 'createdAt']
        read_only_fields = ['id', 'createdAt']

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    subCategoriesCount = serializers.IntegerField(source='subcategories_count', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'subCategoriesCount', 'status', 'createdAt']
        read_only_fields = ['id', 'subCategoriesCount', 'createdAt']


class SubCategorySerializer(serializers.ModelSerializer):
    categoryId = serializers.CharField(source='category_id', read_only=True)
    productCount = serializers.IntegerField(source='product_count', read_only=True)
    
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'categoryId', 'description', 'productCount', 'status']
        read_only_fields = ['id', 'categoryId', 'productCount']
    
    def create(self, validated_data):
        category_id = self.initial_data.get('categoryId')
        if category_id:
            if not Category.objects.filter(id=category_id).exists():
                raise serializers.ValidationError({
                    "error": "Category not found"
                })

            validated_data['category_id'] = category_id
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        category_id = self.initial_data.get('categoryId')
        if category_id:
            if not Category.objects.filter(id=category_id).exists():
                raise serializers.ValidationError({
                    "error": "Category not found"
                })
            validated_data['category_id'] = category_id
        return super().update(instance, validated_data)


class ProductSerializer(serializers.ModelSerializer):
    subCategoryId = serializers.CharField(write_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    subCategory = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'subCategoryId', 'subCategory', 'category',  'capacity', 'price', 'specifications', 'status']
        read_only_fields = ['id', 'category', 'subCategory']
    
    def get_category(self, obj):
        return obj.sub_category.category.name if obj.sub_category else None
    
    def get_subCategory(self, obj):
        return obj.sub_category.name if obj.sub_category else None
    
    def create(self, validated_data):
        subcategory_id = self.initial_data.get('subCategoryId')
        subcategory = SubCategory.objects.get(id=subcategory_id)
        if not subcategory:
            raise serializers.ValidationError({
                "error": "Sub Category not found"
            })

        if subcategory.status == "inactive":
            raise serializers.ValidationError({
                "error": "Sub Category is not active"
            })

        validated_data.pop("subCategoryId", "")
        validated_data['sub_category'] = subcategory
        return super().create(validated_data)

    def update(self, instance, validated_data):
        subcategory_id = self.initial_data.get('subCategoryId')
        subcategory = SubCategory.objects.get(id=subcategory_id)
        if not subcategory:
            raise serializers.ValidationError({
                "error": "Sub Category not found"
            })

        if subcategory.status == "inactive":
            raise serializers.ValidationError({
                "error": "Sub Category is not active"
            })

        validated_data.pop("subCategoryId", "")
        validated_data['sub_category'] = subcategory
        # category_name = self.initial_data.get('category')
        # subcategory_name = self.initial_data.get('subCategory')
        #
        # if category_name:
        #     category, _ = Category.objects.get_or_create(name=category_name, defaults={'status': 'active'})
        #     validated_data['category'] = category
        #
        #     if subcategory_name:
        #         subcategory, _ = SubCategory.objects.get_or_create(
        #             name=subcategory_name,
        #             category=category,
        #             defaults={'status': 'active'}
        #         )
        #         validated_data['sub_category'] = subcategory

        return super().update(instance, validated_data)


class LeadSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    # products = serializers.ListSerializer(child=ProductSerializer, read_only=True)
    productIds = serializers.ListField(child=serializers.CharField(), write_only=True)
    followUpDate = serializers.DateField(source='follow_up_date', required=False, allow_null=True)
    salesRep = serializers.CharField(source='sales_rep', required=False, allow_blank=True, allow_null=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'phone', 'email', 'area', 'address', 'productIds', 'products',
            'status', 'source', 'priority', 'notes', 'followUpDate', 'salesRep', 'createdAt'
        ]
        read_only_fields = ['id', 'createdAt', 'products']

    def get_products(self, obj):
        # Return product data via ProductInterests relation
        products = Product.objects.filter(interested_leads__lead=obj)
        return ProductSerializer(products, many=True).data

    def create(self, validated_data):
        product_ids = validated_data.pop('productIds', [])
        lead = super().create(validated_data)
        for product_id in product_ids:
            product = Product.objects.get(id=product_id)
            ProductInterests.objects.create(
                lead=lead,
                product=product
            )

        return lead

    def update(self, instance, validated_data):
        # Extract product IDs (if provided)
        product_ids = validated_data.pop('productIds', None)

        super().update(instance, validated_data)

        # If product IDs are included in request, update associations
        if product_ids is not None:
            # Remove existing interests
            ProductInterests.objects.filter(lead=instance).delete()

            # Recreate new ones
            for product_id in product_ids:
                try:
                    product = Product.objects.get(id=product_id)
                    ProductInterests.objects.create(lead=instance, product=product)
                except Product.DoesNotExist:
                    # Optional: raise a validation error or ignore missing products
                    raise serializers.ValidationError({"error": f"Product with id {product_id} not found"})

        return instance


class CustomerSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    productIds = serializers.ListField(child=serializers.CharField(), write_only=True)
    installationDate = serializers.DateField(source='installation_date')
    expiryDate = serializers.DateField(source='expiry_date', read_only=True)
    salesRep = serializers.CharField(source='sales_rep', required=False, allow_blank=True, allow_null=True)
    warrantyYears = serializers.IntegerField(write_only=True, required=False, default=2)
    
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'phone', 'email', 'area', 'address', 'productIds', 'products',
            'installationDate', 'expiryDate', 'amount', 'status', 'salesRep', 'notes', 'warrantyYears'
        ]
        read_only_fields = ['id', 'expiryDate', 'products']

    def get_products(self, obj):
        # Return product data via ProductInterests relation
        products = Product.objects.filter(customers__customer=obj)
        return ProductSerializer(products, many=True).data

    def create(self, validated_data):
        warranty_years = validated_data.pop('warrantyYears', 2)
        installation_date = validated_data.get('installation_date')
        
        if installation_date:
            validated_data['expiry_date'] = installation_date + relativedelta(years=warranty_years)

        product_ids = validated_data.pop('productIds', [])
        customer = super().create(validated_data)
        for product_id in product_ids:
            product = Product.objects.get(id=product_id)
            CustomerProducts.objects.create(
                customer=customer,
                product=product
            )
        return customer
    
    def update(self, instance, validated_data):
        warranty_years = validated_data.pop('warrantyYears', None)
        installation_date = validated_data.get('installation_date', instance.installation_date)
        
        if warranty_years and installation_date:
            validated_data['expiry_date'] = installation_date + relativedelta(years=warranty_years)
        product_ids = validated_data.pop('productIds', None)

        super().update(instance, validated_data)

        # If product IDs are included in request, update associations
        if product_ids is not None:
            # Remove existing interests
            CustomerProducts.objects.filter(customer=instance).delete()

            # Recreate new ones
            for product_id in product_ids:
                try:
                    product = Product.objects.get(id=product_id)
                    CustomerProducts.objects.create(customer=instance, product=product)
                except Product.DoesNotExist:
                    # Optional: raise a validation error or ignore missing products
                    raise serializers.ValidationError({"error": f"Product with id {product_id} not found"})

        return instance


class ConvertLeadSerializer(serializers.Serializer):
    installationDate = serializers.DateField()
    warrantyYears = serializers.IntegerField(default=2)
