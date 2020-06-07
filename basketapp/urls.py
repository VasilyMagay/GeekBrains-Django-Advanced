from django.urls import path, re_path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    re_path('^$', basketapp.index, name='index'),
    re_path('^add/(?P<pk>\d+)/$', basketapp.basket_add, name='add'),
    re_path('^remove/(?P<pk>\d+)/$', basketapp.basket_remove, name='remove'),
    re_path('^edit/(?P<product_pk>\d+)/(?P<quantity>\d+)/ajax/$', basketapp.basket_edit),
]

