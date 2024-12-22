from django.db import models
from django.contrib.auth.models import User

# Модель для представления объявления
class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)  
    title = models.CharField(max_length=100, blank=True, default='')  
    body = models.TextField(blank=True, default='')  
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'посты'
        verbose_name = 'пост'
        ordering = ['created']  

    def __str__(self):
        return self.title
    
# Модель для представления отзывов
class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True) 
    body = models.TextField(blank=False)  
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)  
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)  

    def __str__(self):
        return self.body

    class Meta:
        verbose_name_plural = 'комментарии'
        verbose_name = 'комментарий'
        ordering = ['created']  # Сортировка комментариев по дате создания (от старых к новым)

# Модель для представления категории
class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')  # Название категории (максимум 100 символов, не может быть пустым)
    owner = models.ForeignKey('auth.User', related_name='categories', on_delete=models.CASCADE, default=User.objects.first().id)  # Владелец категории (связь с моделью User, при удалении пользователя удаляются все его категории)
    posts = models.ManyToManyField('Post', related_name='categories', blank=True)  # Посты, относящиеся к этой категории (многие-ко-многим связь с моделью Post, может быть пустым)

    class Meta:
        verbose_name_plural = 'категории'
        verbose_name = 'категория'
        verbose_name_plural = 'categories'  # Устанавливает правильное множественное число для названия модели в админке (чтобы не было "Categorys")

    def __str__(self):
        return self.name