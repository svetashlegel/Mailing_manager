from django.core.management import BaseCommand
from django.contrib.auth.models import Group

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        email_adress = input("email ")
        f_name = input("first_name ")
        l_name = input("last_name ")
        password = input("password ")

        user = User.objects.create(
            email=email_adress,
            first_name=f_name,
            last_name=l_name,
            is_staff=True,
            is_active=True
        )

        user.set_password(password)
        user.save()

        manager = Group.objects.get(name='Manager')
        manager.user_set.add(user)
