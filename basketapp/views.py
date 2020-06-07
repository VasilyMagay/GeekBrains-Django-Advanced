from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from mainapp.models import Product
from basketapp.models import Basket
# from mainapp.views import get_basket
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import F


@login_required
def index(request):
    # basket = get_basket(request.user)
    context = {
        # 'basket': basket,
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:product',
                                            kwargs={
                                                'pk': pk,
                                            }))
    # print(f'поймали продукт: {product_pk}')
    # print(request.META.keys())
    # return HttpResponseRedirect('/')
    # product = Product.objects.filter(pk=product_pk).first()
    # product = Product.objects.get(pk=product_pk)
    product = get_object_or_404(Product, pk=pk)
    basket_item = Basket.objects.filter(product=product, user=request.user).first()
    if basket_item:
        basket_item.quantity = F('quantity') + 1
        # basket_item.quantity += 1
        basket_item.save()
        print(f'обновлен объект корзины')
    else:
        Basket.objects.create(product=product, user=request.user, quantity=1)
        print(f'создан новый объект корзины')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])  # Возвращаемся туда откуда пришли.


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, product_pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(product_pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        context = {
            # 'basket': get_basket(request.user),
            'basket': request.user.basket_set.all().order_by('product__category'),
        }
        result = render_to_string('basketapp/inc/inc__basket_list.html', context)

        return JsonResponse({
            'result': result
        })
