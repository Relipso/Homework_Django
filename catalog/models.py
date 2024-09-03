from django.db import models
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Product(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание"
    )
    preview = models.ImageField(
        upload_to="media",
        blank=True,
        null=True,
        verbose_name="Изображение (превью)",
        help_text="Добавьте изображение",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
        help_text="Введите категорию",
    )
    price = models.DecimalField(
        verbose_name="Цена", max_digits=10, decimal_places=2, help_text="Введите цену"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания", help_text="Введите дату"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
        help_text="Введите дату изменения",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Владелец",
        help_text="Выберите владельца продукта",
        **NULLABLE
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Статус публикации продукта"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]
        permissions = (
            ("can_unpublish_product", "Отменить публикацию"),
            ("can_change_product_description", "Изменить описание"),
            ("can_change_product_category", "Изменить категорию"),
        )


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание категории"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Наименование продукта",
        related_name="version",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )
    version_number = models.PositiveIntegerField(
        default=0,
        verbose_name="Номер версии продукта",
        help_text="Введите номер версии продукта",
        **NULLABLE,
    )
    version_name = models.CharField(
        max_length=50,
        verbose_name="Наименование версии продукта",
        help_text="Введите наименование версии продукта",
        **NULLABLE,
    )
    version_sign = models.BooleanField(
        verbose_name="признак текущей версии", help_text="Версия активна?", default=True
    )

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ["product", "version_number", "version_name"]

    def __str__(self):
        return self.version_name
