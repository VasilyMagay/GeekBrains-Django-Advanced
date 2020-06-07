from django.contrib import admin
from django.urls import path, re_path
import mainapp.views as mainapp
# from django.views.decorators.cache import cache_page

app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', mainapp.index, name='index'),

    re_path(r'^products/$', mainapp.products, name='products'),

    re_path(r'^catalog/category/(?P<category_pk>\d+)/$', mainapp.products, name='catalog'),
    # re_path(r'^catalog/category/(?P<category_pk>\d+)/ajax/$', cache_page(3600)(mainapp.products_ajax)),

    re_path(r'^catalog/category/(?P<category_pk>\d+)/page/(?P<page>\d+)/$', mainapp.products, name='catalog'),
    # re_path(r'^catalog/category/(?P<category_pk>\d+)/page/(?P<page>\d+)/ajax/$',
    # cache_page(3600)(mainapp.products_ajax)),

    # re_path(r'^catalog/category/(?P<category_pk>\d+)/page/(?P<page>\d+)/$', mainapp.products, name='catalog'),

    # ?P<pk> - именованный параметр
    re_path(r'^catalog/product/(?P<pk>\d+)/$', mainapp.product, name='product'),

    re_path(r'^contact/$', mainapp.contact, name='contact'),
]
