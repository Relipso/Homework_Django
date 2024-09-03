from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создает группу Модератор с необходимыми разрешениями'

    def handle(self, *args, **options):
        moderator_group, created = Group.objects.get_or_create(name="Модератор")

        if created:
            self.stdout.write(self.style.SUCCESS('Группа Модератор успешно создана'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа Модератор уже существует'))

        permissions = [
            'can_change_product_description',
            'can_change_product_category',
            'can_unpublish_product'
        ]

        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            moderator_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Разрешения добавлены к группе Модератор'))

        all_permissions = moderator_group.permissions.all()
        self.stdout.write(self.style.SUCCESS('Все разрешения для группы Модератор:'))
        for perm in all_permissions:
            self.stdout.write(f'- {perm.codename}')
