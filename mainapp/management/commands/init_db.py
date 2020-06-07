from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
# from django.contrib.auth.models import User
from authapp.models import ShopUser
import json
import os
import csv


JSON_PATH = 'json'
CSV_PATH = 'csv'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):

        ProductCategory.objects.all().delete()

        category_new = 0
        with open(os.path.join(CSV_PATH, 'categories.csv'), "r", newline="") as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                ProductCategory.objects.create(name=row["name"]).save()
                category_new += 1
        print('Добавлено {} категорий продуктов'.format(category_new))

        Product.objects.all().delete()

        product_new = 0
        with open(os.path.join(CSV_PATH, 'products.csv'), "r", newline="") as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                # print(row["price"], type(row["price"]), float(row["price"]))
                new_product = Product.objects.create(
                    category=ProductCategory.objects.get(name=row["category"]),
                    name=row["name"],
                    short_desc=row["short_desc"],
                    description=row["description"],
                    price=float(row["price"]),
                    quantity=int(row["quantity"]))
                new_product.save()
                product_new += 1
        print('Добавлено {} продуктов'.format(product_new))

        # # Создаем суперпользователя при помощи менеджера модели
        # user = User.objects.filter(username='django')
        # if not user:
        #     print('создан новый суперпользователь')
        #     User.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains')

        # Создаем суперпользователя при помощи менеджера модели
        user = ShopUser.objects.filter(username='django')
        if not user:
            print('создан новый суперпользователь')
            ShopUser.objects.create_superuser('django', 'django@geekshop.local',
                                              'geekbrains', age=21)
