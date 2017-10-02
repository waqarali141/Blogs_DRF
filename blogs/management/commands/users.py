# -*- coding: utf-8 -*-
__author__ = 'waqarali'


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Shows Employees list'
    users = [('hamza', '1234qwer'), ('badr', '1234qwer'), ('badr1', '1234qwer'), ('badr2', '1234qwer'),
             ('badr3', '1234qwer'), ('zunair', '1234qwer'), ('zunair1', '1234qwer'), ('zunair2', '1234qwer'),
             ('zunair3', '1234qwer'), ('waqar', '1234qwer'), ('waqar1', '1234qwer'), ('waqar2', '1234qwer')
             ]

    def handle(self, *args, **options):
        for (username, password) in self.users:
            user_object = User.objects.create_user(username=username, password=password)
            if username == 'waqar':
                user_object.is_superuser = True
                user_object.is_active = True
                user_object.is_staff = True
                user_object.save()
            self.stdout.write(self.style.SUCCESS("Created user with username: %s" % user_object.username))
