from rest_framework import serializers
from products.models import Product


class BaseProductSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        product_data = Product.objects.filter(sku = instance.sku)
        product_data = product_data.update(**validated_data)
        product_data = Product.objects.using('storage').filter(sku = instance.sku)
        product_data = product_data.update(**validated_data)
        return validated_data
    
    def update_to_memory(self, instance, validated_data):
        product_data = Product.objects.filter(sku = instance.sku)
        product_data = product_data.update(**validated_data)
        return validated_data


class ProductSerializer(BaseProductSerializer):
    class Meta:
        model = Product
        fields = ('id', 'sku', 'name', 'qty', 'price')
        
    def save_to_memory(self, validated_data):
        product_data = Product(**validated_data)
        product_data.save()
        return product_data

    def create(self, validated_data):
        product_data = Product(**validated_data)
        product_data.save()
        product_data.save(using='storage')
        return product_data

class UpdateProductSerializer(BaseProductSerializer):
    class Meta:
        model = Product
        fields = ('qty', )


class UpdateSerializer(serializers.Serializer):
    update_qty = serializers.IntegerField(min_value=0,default=None, required=False, allow_null=True)
    add_qty = serializers.IntegerField(default=None, required=False, allow_null=True)
