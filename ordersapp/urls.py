from django.urls import re_path
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    re_path('^list/$', ordersapp.OrderList.as_view(), name='index'),
    re_path('^create/$', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
    re_path('^read/(?P<pk>\d+)/$', ordersapp.OrderRead.as_view(), name='order_read'),
    re_path('^update/(?P<pk>\d+)/$', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),
    re_path('^delete/(?P<pk>\d+)/$', ordersapp.OrderDelete.as_view(), name='order_delete'),

    re_path('^order/proceed/(?P<pk>\d+)/$', ordersapp.order_forming_complete, name='order_forming_complete'),
    # Служебная ссылка для получения цены товара
    re_path('^product/(?P<pk>\d+)/price/$', ordersapp.get_product_price),
]

