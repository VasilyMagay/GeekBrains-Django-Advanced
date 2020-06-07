from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

from adminapp.forms import AdminShopUserRegisterForm, AdminShopUserChangeForm, AdminProductCategoryEditForm, AdminProductEditForm
from django.contrib.auth.decorators import user_passes_test

# CBV
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from django.db.models import F


# @user_passes_test(lambda x: x.is_superuser)
# def index(request):
#     object_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': 'админка/пользователи',
#         'object_list': object_list
#     }
#     return render(request, 'adminapp/users.html', context)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersListView(ListView):
    model = ShopUser
    # template_name = 'adminapp/users.html'

    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context

    def get_ordering(self):
        return ['-is_active', '-is_superuser', '-is_staff', 'username']


# def user_create(request):
#     if request.method == 'POST':
#         form = AdminShopUserRegisterForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin:index'))
#     else:
#         form = AdminShopUserRegisterForm()
#
#     context = {
#         'title': 'пользователи/создание',
#         'form': form
#     }
#
#     return render(request, 'adminapp/user_update.html', context)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserCreateView(CreateView):
    model = ShopUser
    success_url = reverse_lazy('admin:index')
    form_class = AdminShopUserRegisterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/создание'
        return context


# def user_update(request, pk):
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         form = AdminShopUserChangeForm(request.POST, request.FILES, instance=edit_user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin:user_update',
#                                                 kwargs={
#                                                     'pk': edit_user.pk,
#                                                 }))
#     else:
#         form = AdminShopUserChangeForm(instance=edit_user)
#
#     content = {
#         'title': 'пользователи/редактирование',
#         'form': form
#     }
#
#     return render(request, 'adminapp/user_update.html', content)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserUpdateView(UpdateView):
    model = ShopUser
    success_url = reverse_lazy('admin:index')
    form_class = AdminShopUserChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context


# def user_delete(request, pk):
#     user = get_object_or_404(ShopUser, pk=pk)
#     # user.is_active = False
#     # user.save()
#     # return HttpResponseRedirect(reverse('admin:index'))
#     if request.method == 'POST':
#         # user.delete()
#         # вместо удаления лучше сделаем неактивным
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin:index'))
#
#     context = {
#         'title': 'пользователи/удаление',
#         'user_to_delete': user
#     }
#
#     return render(request, 'adminapp/user_delete.html', context)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserDeleteView(DeleteView):
    model = ShopUser
    success_url = reverse_lazy('admin:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/удаление'
        return context


# def user_undelete(request, pk):
#     current_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         current_user.is_active = True
#         current_user.save()
#         return HttpResponseRedirect(reverse('admin:index'))
#
#     context = {
#         'title': 'пользователи/восстановление',
#         'current_user': current_user
#     }
#
#     return render(request, 'adminapp/user_undelete.html', context)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserUndeleteView(DeleteView):
    model = ShopUser
    success_url = reverse_lazy('admin:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/восстановление'
        context['undelete'] = True
        return context


# @user_passes_test(lambda x: x.is_superuser)
# def categories(request):
#     categories_list = ProductCategory.objects.all().order_by('-is_active', 'name')
#
#     context = {
#         'title': 'админка/категории',
#         'object_list': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', context)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoriesListView(ListView):
    model = ProductCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context

    def get_ordering(self):
        return ['-is_active', 'name']


# def category_create(request):
#     if request.method == 'POST':
#         form = AdminProductCategoryEditForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         form = AdminProductCategoryEditForm()
#
#     content = {
#         'title': 'категории/создание',
#         'form': form
#     }
#
#     return render(request, 'adminapp/category_update.html', content)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    success_url = reverse_lazy('admin:categories')
    form_class = AdminProductCategoryEditForm
    # template_name = 'adminapp/category_update.html'
    # fields = ('__all__')  # Указывается либо fields, либо form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context


# def category_update(request, pk):
#     edit_obj = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         form = AdminProductCategoryEditForm(request.POST, request.FILES, instance=edit_obj)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin:category_update',
#                                                 kwargs={
#                                                     'pk': edit_obj.pk,
#                                                 }))
#     else:
#         form = AdminProductCategoryEditForm(instance=edit_obj)
#
#     content = {
#         'title': 'категории/редактирование',
#         'form': form
#     }
#
#     return render(request, 'adminapp/category_update.html', content)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    success_url = reverse_lazy('admin:categories')
    form_class = AdminProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

# def category_delete(request, pk):
#     object_to_delete = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         object_to_delete.is_active = False
#         object_to_delete.product_set.all().update(is_active=False)  # помечаем все связанные продукты
#         object_to_delete.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         pass
#         object_to_delete.product_set.all().update(is_active=True)
#
#     context = {
#         'title': 'категории/удаление',
#         'object_to_delete': object_to_delete
#     }
#
#     return render(request, 'adminapp/category_delete.html', context)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('admin:categories')
    # template_name = 'adminapp/category_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        # self.object.product_set.all().update(is_active=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/удаление'
        return context


# def category_undelete(request, pk):
#     current_object = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         current_object.is_active = True
#         current_object.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     context = {
#         'title': 'категории/восстановление',
#         'current_object': current_object
#     }
#
#     return render(request, 'adminapp/category_undelete.html', context)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryUndeleteView(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        # self.object.product_set.all().update(is_active=True)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/восстановление'
        context['undelete'] = True
        return context


# @user_passes_test(lambda x: x.is_superuser)
# def products(request, pk):
#     category = get_object_or_404(ProductCategory, pk=pk)
#     object_list = Product.objects.filter(category__pk=pk).order_by('-is_active', 'name')
#
#     content = {
#         'title': 'админка/продукт',
#         'category': category,
#         'object_list': object_list,
#     }
#
#     return render(request, 'adminapp/products.html', content)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductsListView(ListView):
    model = Product
    category = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print('CONTEXT==', self.category)
        context['title'] = 'админка/продукт'
        context['category'] = get_object_or_404(ProductCategory, pk=self.category)
        return context

    def get_ordering(self):
        return ['-is_active', 'name']

    def get_queryset(self):
        # print('KWARGS=', self.kwargs['pk'])
        self.category = self.kwargs['pk']
        return Product.objects.filter(category__pk=self.category)


# def product_read(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#
#     context = {
#         'title': 'продукт/подробнее',
#         'object': product,
#     }
#
#     return render(request, 'adminapp/product_read.html', context)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    # template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/подробнее'
        return context


# def product_create(request, pk):
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         form = AdminProductEditForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         # задаем начальное значение категории в форме
#         form = AdminProductEditForm(initial={'category': category})
#
#     context = {
#         'title': 'продукт/создание',
#         'form': form,
#         'category': category
#     }
#
#     return render(request, 'adminapp/product_update.html', context)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    category = None
    # success_url = reverse_lazy('admin:products')
    form_class = AdminProductEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/создание'
        context['category'] = get_object_or_404(ProductCategory, pk=self.category)
        return context

    def get_initial(self):
        self.category = self.kwargs['pk']
        initial = self.initial.copy()
        initial['category'] = self.category
        return initial

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('admin:products', args=[self.category]))


# def product_update(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         form = AdminProductEditForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin:products',
#                                                 kwargs={
#                                                     'pk': product.category.pk
#                                                 }))
#     else:
#         form = AdminProductEditForm(instance=product)
#
#     context = {
#         'title': 'продукт/редактирование',
#         'form': form,
#         'category': product.category,
#     }
#
#     return render(request, 'adminapp/product_update.html', context)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    # success_url = reverse_lazy('admin:products')
    form_class = AdminProductEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/редактирование'
        context['category'] = self.object.category
        return context

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('admin:products', kwargs={'pk': self.object.category.pk}))


# def product_delete(request, pk):
#     item = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         item.is_active = False
#         item.save()
#         return HttpResponseRedirect(reverse('admin:products',
#                                             kwargs={
#                                                 'pk': item.category.pk
#                                             }))
#
#     context = {
#         'title': 'продукт/удаление',
#         'object': item
#     }
#
#     return render(request, 'adminapp/product_delete.html', context)
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    # success_url = reverse_lazy('admin:products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(reverse('admin:products', kwargs={'pk': self.object.category.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/удаление'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductUndeleteView(DeleteView):
    model = Product
    # success_url = reverse_lazy('admin:products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse('admin:products', kwargs={'pk': self.object.category.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/восстановление'
        context['undelete'] = True
        return context


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
