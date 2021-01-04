from django.apps import AppConfig
from django.core.management import call_command
import sys
import os
import json

class ProductsConfig(AppConfig):
    name = 'products'

    # on server start migrate and dump storage db and load data to memory db 
    # couldnt use call_command('loaddata') as it run migrations checks and reload server.
    def ready(self):
        super().ready()
        if 'runserver' not in sys.argv:
            return True
        else:
            from products.serializers import ProductSerializer
            call_command('migrate',
                app_label='products',
                verbosity=0,
                interactive=True,
                database='default')
            call_command('dumpdata',
                'products',
                output='products.json',
                verbosity=0,
                database='storage',
                format='json')
            if os.path.exists('products.json'):
                with open('products.json', 'r') as myfile:
                    data=json.loads(myfile.read())
                    for item in data:
                        if item['model'] == 'products.product':
                            serializer = ProductSerializer(data=item['fields'])
                            if serializer.is_valid():
                                serializer.save_to_memory(item['fields'])
                            else: 
                                print(serializer.errors)