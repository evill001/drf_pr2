# Руководство программиста для Avito API

## Введение

Это руководство предназначено для разработчиков, которые будут работать с API, созданным с использованием Django и Django REST Framework. В руководстве описаны основные аспекты работы с классами `generics`, управление правами доступа (`permissions`), а также инструкции по тестированию API с использованием Postman.

## Содержание

1. [Схема базы данных](#схема-базы-данных)
2. [Работа с классами `generics`](#работа-с-классами-generics)
3. [Назначение прав доступа (`permissions`)](#назначение-прав-доступа-permissions)
4. [Работа в Postman](#работа-в-postman)

## Схема базы данных

### Таблицы:
- **User**: Таблица пользователей.
- **Ad**: Таблица объявлений.
- **Review**: Таблица отзывов.
- **Category**: Таблица категорий.

### Связи:
- **Ad** связан с **User** через поле `owner` (один ко многим).
- **Review** связан с **User** через поле `owner` (один ко многим).
- **Review** связан с **Ad** через поле `ad` (один ко многим).
- **Category** связан с **User** через поле `owner` (один ко многим).
- **Category** связан с **Ad** через поле `ads` (многие ко многим).

## Работа с классами `generics`

Django REST Framework предоставляет классы `generics`, которые упрощают создание представлений (views) для CRUD-операций. Вот примеры использования:

### Примеры классов `generics`:

```python
from rest_framework import generics
from .models import Ad, Review, Category
from .serializers import AdSerializer, ReviewSerializer, CategorySerializer

# Представление для списка всех объявлений и создания нового объявления
class AdList(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

# Представление для отображения, обновления и удаления конкретного объявления
class AdDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

# Представление для списка всех отзывов и создания нового отзыва
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Представление для отображения, обновления и удаления конкретного отзыва
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Представление для списка всех категорий и создания новой категории
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Представление для отображения, обновления и удаления конкретной категории
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```

### Описание:
- **ListCreateAPIView**: Используется для отображения списка объектов и создания новых объектов.
- **RetrieveUpdateDestroyAPIView**: Используется для отображения, обновления и удаления конкретного объекта.

## Назначение прав доступа (`permissions`)

Права доступа управляют тем, кто может выполнять определенные действия с объектами. В Django REST Framework есть несколько встроенных разрешений, а также возможность создавать собственные.

### Примеры разрешений:

```python
from rest_framework import permissions

# Разрешение, которое позволяет только владельцу объекта его редактировать или удалять
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

# Применение разрешений в представлениях
class AdDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
```

### Описание:
- **IsAuthenticatedOrReadOnly**: Разрешает доступ только аутентифицированным пользователям для изменения данных, а всем остальным – только чтение.
- **IsOwnerOrReadOnly**: Разрешает доступ к объекту только его владельцу для изменения или удаления.

## Работа в Postman

Postman – это инструмент для тестирования API. Вот как можно использовать Postman для работы с вашим API:

### 1. Установка и настройка Postman
- Скачайте и установите Postman с [официального сайта](https://www.postman.com/downloads/).
- Создайте новый рабочий профиль и настройте окружение для вашего API.

### 2. Тестирование API

#### Получение списка объявлений
- **Метод**: GET
- **URL**: `http://localhost:8000/ads/`
- **Описание**: Получение списка всех объявлений.

#### Создание нового объявления
- **Метод**: POST
- **URL**: `http://localhost:8000/ads/`
- **Тело запроса**:
  ```json
  {
      "title": "Новое объявление",
      "body": "Это тело нового объявления"
  }
  ```
- **Описание**: Создание нового объявления.

#### Получение конкретного объявления
- **Метод**: GET
- **URL**: `http://localhost:8000/ads/<id>/`
- **Описание**: Получение информации о конкретном объявлении по его ID.

#### Обновление объявления
- **Метод**: PUT
- **URL**: `http://localhost:8000/ads/<id>/`
- **Тело запроса**:
  ```json
  {
      "title": "Обновленное объявление",
      "body": "Это обновленное тело объявления"
  }
  ```
- **Описание**: Обновление информации о конкретном объявлении по его ID.

#### Удаление объявления
- **Метод**: DELETE
- **URL**: `http://localhost:8000/ads/<id>/`
- **Описание**: Удаление конкретного объявления по его ID.

### 3. Аутентификация
- Если ваше API требует аутентификации, используйте вкладку `Authorization` в Postman для настройки токена или базовой аутентификации.

### 4. Тестирование других ресурсов
- Аналогично тестируйте другие ресурсы, такие как отзывы и категории, используя соответствующие URL и методы.

## Заключение

Это руководство предоставляет основные инструкции по работе с API, созданным с использованием Django и Django REST Framework. Используя классы `generics` и правильно настроенные разрешения, вы можете легко управлять доступом к вашим ресурсам. Postman поможет вам тестировать и отлаживать ваше API.