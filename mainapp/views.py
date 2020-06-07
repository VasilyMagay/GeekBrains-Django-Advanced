from django.shortcuts import render, get_object_or_404
import json
from mainapp.models import ProductCategory, Product
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from django.core.cache import cache

from django.template.loader import render_to_string
# from django.views.decorators.cache import cache_page
from django.http import JsonResponse


# def get_basket(user):
#     if user.is_authenticated:
#         return user.basket_set.all().order_by('product__category')
#     return []

def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = get_products()

    return random.sample(list(products), 1)[0]


def index(request):

    # basket = get_basket(request.user)

    context = {
        'page_title': 'главная',
        # 'basket': basket,
    }
    return render(request, 'mainapp/index.html', context)


# @cache_page(3600)
def products(request, category_pk=None, page=1):

    # basket = get_basket(request.user)

    categories = ProductCategory.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)

    if category_pk:
        if category_pk != '0':
            products = Product.objects.filter(category_id=category_pk, is_active=True)
            # products = get_products_ordered_by_price()

        products_paginator = Paginator(products, 2)

        try:
            products = products_paginator.get_page(page)
        except PageNotAnInteger:
            products = products_paginator.get_page(1)
        except EmptyPage:
            products = products_paginator.get_page(products_paginator.num_pages)

        context = {
            'page_title': ' | каталог',
            'products': products,
            'categories': categories,
            # 'basket': basket,
            'category_pk': category_pk,
        }
        return render(request, 'mainapp/products_list.html', context)
    else:
        # hot_product = random.choice(products)
        hot_product = get_hot_product()
        same_products = Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)

        context = {
            'page_title': ' | каталог',
            'categories': categories,
            # 'basket': basket,
            'hot_product': hot_product,
            'same_products': same_products,
        }
        return render(request, 'mainapp/products.html', context)


def products_ajax(request, category_pk=None, page=1):
    if request.is_ajax():

        categories = ProductCategory.objects.filter(is_active=True)
        products = Product.objects.filter(is_active=True)

        if category_pk:
            if category_pk != '0':
                products = get_products_ordered_by_price()

            products_paginator = Paginator(products, 2)

            try:
                products = products_paginator.get_page(page)
            except PageNotAnInteger:
                products = products_paginator.get_page(1)
            except EmptyPage:
                products = products_paginator.get_page(products_paginator.num_pages)

            context = {
                'page_title': ' | каталог',
                'products': products,
                'categories': categories,
                # 'basket': basket,
                'category_pk': category_pk,
            }
            result = render_to_string(
                'mainapp/inc/inc__products_list_content.html',
                context=context,
                request=request
            )
            return JsonResponse({'result': result})
        else:
            # hot_product = random.choice(products)
            hot_product = get_hot_product()
            same_products = Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)

            context = {
                'page_title': ' | каталог',
                'categories': categories,
                # 'basket': basket,
                'hot_product': hot_product,
                'same_products': same_products,
            }
            return render(request, 'mainapp/products.html', context)


def product(request, pk):

    categories = ProductCategory.objects.filter(is_active=True)
    # basket = get_basket(request.user)
    # product = Product.objects.filter(pk=pk).select_related().first()
    product = get_product(pk)

    context = {
        'title': 'продукт',
        'categories': categories,
        'product': product,
        # 'product': get_object_or_404(Product, pk=pk),
        # 'basket': basket,
    }

    return render(request, 'mainapp/product.html', context)


def contact(request):

    # basket = get_basket(request.user)

    # locations = [
    #     {
    #         'city': 'Москва',
    #         'phone': '+7-495-100-10-10',
    #         'email': 'moscow@catalog.ru',
    #         'address': 'В пределах МКАД',
    #     },
    #     {
    #         'city': 'Санкт-Петербург',
    #         'phone': '+7-812-200-20-20',
    #         'email': 'spb@catalog.ru',
    #         'address': 'В пределах КАД',
    #     },
    #     {
    #         'city': 'Псков',
    #         'phone': '+7-987-300-30-30',
    #         'email': 'pskov@catalog.ru',
    #         'address': 'У стен кремля',
    #     }
    # ]
    #
    # with open('json/locations.json', 'w', encoding='utf-8') as tmp_file:
    #     json.dump(locations, tmp_file)

    if settings.LOW_CACHE:
        key = f'locations'
        locations = cache.get(key)
        if locations is None:
            with open('json/locations.json', 'r', encoding='utf-8') as tmp_file:
                locations = json.load(tmp_file)
            cache.set(key, locations)
    else:
        with open('json/locations.json', 'r', encoding='utf-8') as tmp_file:
            locations = json.load(tmp_file)

    context = {
        'page_title': ' | контакты',
        'locations': locations,
        # 'basket': basket,
    }

    return render(request, 'mainapp/contact.html', context)
