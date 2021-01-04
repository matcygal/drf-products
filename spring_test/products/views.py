from products.models import Product
from products.serializers import ProductSerializer, UpdateProductSerializer, UpdateSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



filter_param = openapi.Parameter(
    'filter',
    openapi.IN_QUERY,
    description="Filter parameter - accepted values: 'available' and 'sold_out'",
    required=False,
    type=openapi.TYPE_STRING,
)

class ProductViewSet(viewsets.ViewSet):
    lookup_field = 'sku'
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @swagger_auto_schema(manual_parameters=[filter_param], 
        operation_summary="Get list of products",
        operation_description="Get parameter - filter (optional) is accepting 2 values: available or sold_out",
        )    
    def list(self, request):
        """Getting list of all products"""
        products = Product.objects
        filter = request.query_params.get('filter')
        if filter == "available":
            products = products.filter(qty__gt=0)
        elif filter == "sold_out":
            products = products.filter(qty=0)

        products = products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductSerializer,
        operation_summary="Create new product",
        operation_description="SKU has to be unique, and max 16 alphanumeric characters, name has to be max 255 characters, qty has to be allways bigger than 0, price need to be decimal string",
        )
    def create(self, request):
        """Create new product"""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            if request.META['SERVER_NAME'] == "testserver":
                serializer.save_to_memory(serializer.data)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Get product by SKU",
        operation_description="SKU has to be unique, and max 16 alphanumeric characters",
        )
    def retrieve(self, request, sku=None):
        """Get product by SKU"""
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, sku=sku)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductSerializer,         
        operation_summary="Update product by SKU",
        operation_description="SKU has to be unique, and max 16 alphanumeric characters, name has to be max 255 characters, qty has to be allways bigger than 0, price need to be decimal string",
        )
    def update(self, request, sku=None):
        """Update whole product"""
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, sku=sku)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            if request.META['SERVER_NAME'] == "testserver":
                serializer.update_to_memory(product, serializer.validated_data)
            else:
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=UpdateSerializer,
        operation_summary="Partial update product by SKU",
        operation_description="SKU has to be unique, and max 16 alphanumeric characters, body accept two values: update_qty: int - which replace old value or add_qty: int - which adding quantity, those values cannot be use togheter.",
        )
    def partial_update(self, request, sku=None):
        """Update or add quantity"""
        if request.data.get('update_qty') and request.data.get('add_qty'):
            return Response({"error": "Cannot update and add at the same time"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, sku=sku)
        if request.data.get('update_qty'):
            data = {"qty" : request.data.get('update_qty')}
        elif request.data.get('add_qty'):
            data = {"qty" : int(product.qty) + int(request.data.get('add_qty'))}
        else:
            return Response({"error": "nothing to update"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateProductSerializer(product, data=data)
        if serializer.is_valid():
            if request.META['SERVER_NAME'] == "testserver":
                serializer.update_to_memory(product, serializer.validated_data)
            else:
                serializer.save()
            result = {'sku' : sku}
            result.update(serializer.validated_data)
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete product by SKU",
        operation_description="SKU has to be unique, and max 16 alphanumeric characters",
        )
    def destroy(self, request, sku=None):
        """Delete product by SKU"""
        if request.META['SERVER_NAME'] != "testserver":
            queryset = Product.objects.using('storage').all()
            product = get_object_or_404(queryset, sku=sku)
            product.delete()

        queryset = Product.objects.all()
        product = get_object_or_404(queryset, sku=sku)
        product.delete()
        return Response({"msg": "Object with SKU {} has been deleted".format(sku)}, status=status.HTTP_204_NO_CONTENT)