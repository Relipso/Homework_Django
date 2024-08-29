from django.db import models

NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Заголовок",
        help_text="Введите заголовок",
        **NULLABLE,
    )
    slug = models.CharField(
        max_length=150,
        verbose_name="Идентификатор",
        **NULLABLE,
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите содержимое",
        **NULLABLE,
    )
    image = models.ImageField(
        upload_to="products/photo",
        verbose_name="Изображение",
        help_text="Загрузите изображение",
        **NULLABLE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    is_publication = models.BooleanField(
        verbose_name="Создать?",
        default=False,
    )
    count_views = models.IntegerField(
        default=0,
        verbose_name="Количество просмотров",
        help_text="Укажите количество просмотров",
    )

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

    def __str__(self):
        return self.title or f"Blog {self.id}"
