from django.core.management.base import BaseCommand
from authapp.models import ShopUser
from authapp.models import ShopUserProfile


class Command(BaseCommand):
    help = 'Update user base (new user profile)'

    def handle(self, *args, **options):
        users = ShopUser.objects.filter(shopuserprofile__isnull=True)
        for user in users:
            ShopUserProfile.objects.create(user=user)
