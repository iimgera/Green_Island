from django.db import models
from django.core.validators import RegexValidator


class Category(models.Model):
    name = models.CharField(
        max_length=70, verbose_name='Название'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Section(models.Model):
    title = models.CharField(
        max_length=65, verbose_name='Заголовок',
    )
    description = models.TextField(verbose_name='Текст')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='section_name', verbose_name='Категория'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Секция деятельности'
        verbose_name_plural = 'Секция деятельности'


class Rules(models.Model):
    title = models.CharField(
        max_length=65, verbose_name='Заголовок',
    )
    image = models.ImageField(
        upload_to='articles/%Y/%m/%d/',
        verbose_name='Изображение',
    )
    description = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Правила сортировки'
        verbose_name_plural = 'Правила сортировки'


class Contact(models.Model):
    address = models.CharField(
        max_length=155, verbose_name='Наш адрес'
    )
    phone = models.CharField(
        max_length=15, validators=[RegexValidator(r'^[0-9()+]+$', 'Enter a valid phone number.')],
        verbose_name='Номер телефона',
    )
    email = models.EmailField(verbose_name='Наш email')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Point(models.Model):
    link = models.URLField(
        max_length=70, verbose_name='Адрес'
    )

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = 'Точка приема'
        verbose_name_plural = 'Точки приема'
