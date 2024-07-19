from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        return [
            {'name': 'Еда', 'description': 'Это еда'},
            {'name': 'Инструмент', 'description': 'Это инструмент'},
            {'name': 'Животные', 'description': 'Это животные'},
        ]

    @staticmethod
    def json_read_products():
        return [
            {'name': 'Хлеб', 'description': 'Это хлеб', 'category': 'Еда', 'price': 30.99},
            {'name': 'Молоко', 'description': 'Это молоко', 'category': 'Еда', 'price': 60.99},
            {'name': 'Молоток', 'description': 'Это молоток', 'category': 'Инструмент', 'price': 1499.99},
            {'name': 'Пила', 'description': 'Это пила', 'category': 'Инструмент', 'price': 1599.99},
            {'name': 'Лошадь', 'description': 'Это лошадь', 'category': 'Животные', 'price': 110000},
            {'name': 'Курица', 'description': 'Это курица', 'category': 'Животные', 'price': 1500},
        ]

    def handle(self, *args, **options):
        # Удаление старых данных
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Загружаем и создаем категории
        categories_data = self.json_read_categories()
        for category_data in categories_data:
            category_for_create.append(
                Category(name=category_data['name'], description=category_data['description'])
            )

        # Создаем категории в базе данных
        Category.objects.bulk_create(category_for_create)

        # Загружаем и создаем продукты
        products_data = self.json_read_products()
        for product_data in products_data:
            # Получаем категорию из базы данных для корректной связки
            category = Category.objects.get(name=product_data['category'])
            product_for_create.append(
                Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    category=category,
                    price=product_data['price']
                )
            )

        # Создаем продукты в базе данных
        Product.objects.bulk_create(product_for_create)

        self.stdout.write(self.style.SUCCESS('Database populated successfully'))
