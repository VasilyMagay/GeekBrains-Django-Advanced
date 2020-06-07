from django import template

register = template.Library()

from django.conf import settings

URL_PREFIX = settings.MEDIA_URL
# URL_PREFIX = '/media/'


@register.filter(name='media_folder_products')
def media_folder_products(string):
    if not string:
        string = 'products_images/default.jpg'
    return f"{URL_PREFIX}{string}"


@register.filter(name='media_folder_users')
def media_folder_users(string):
    if not string:
        string = 'users_avatars/default.jpg'
    return f"{URL_PREFIX}{string}"


# Еще один способ регистрации шаблонного фильтра
# register.filter('media_folder_products', media_folder_products)
# register.filter('media_folder_users', media_folder_users)