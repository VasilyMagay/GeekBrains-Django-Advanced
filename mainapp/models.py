from django.db import models


class ProductCategory(models.Model):

    name = models.CharField(verbose_name='имя категории', max_length=128, unique=True)  # аналог varchar

    # null=True - может быть NULL, black=True - пустая строка
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
            return f'ProductCategory: {self.name} ({self.pk})'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, verbose_name='категория продукта',
                                 on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)  # относительный адрес изображения в папке /media
    short_desc = models.CharField(verbose_name='краткое описание продукта',
                                  max_length=64, blank=True)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта',
                                max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    def __str__(self):
            return f'[{self.category.name}] {self.name} ({self.pk})'

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).select_related().order_by('category__name', 'name')
        # return Product.objects.filter(is_active=True).order_by('category__name', 'name')
