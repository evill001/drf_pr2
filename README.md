---
# Руководство программиста для Avito API

---
## Введение

Это руководство предназначено для разработчиков, которые будут работать с API, созданным с использованием Django и Django REST Framework. В руководстве описаны основные аспекты работы с классами `generics`, управление правами доступа (`permissions`), а также инструкции по тестированию API с использованием Postman.

---
## Содержание

1. [Схема базы данных](#схема-базы-данных)
2. [Работа с классами `generics`](#работа-с-классами-generics)
3. [Назначение прав доступа (`permissions`)](#назначение-прав-доступа-permissions)
4. [Работа в Postman](#работа-в-postman)

---
## Схема базы данных

### Основные таблицы

- **User**: Таблица пользователей.
- **Ad**: Таблица объявлений.
- **Review**: Таблица отзывов.
- **Category**: Таблица категорий.

### Связи между таблицами

- **Ad** связан с **User** через поле `owner` (один ко многим).
- **Review** связан с **User** через поле `owner` (один ко многим).
- **Review** связан с **Ad** через поле `ad` (один ко многим).
- **Category** связан с **User** через поле `owner` (один ко многим).
- **Category** связан с **Ad** через поле `ads` (многие ко многим).

---
## Работа с классами `generics`

Django REST Framework предоставляет мощные классы `generics`, которые значительно упрощают создание CRUD-представлений. Вот несколько примеров их использования:

### Примеры классов `generics`

```python
from rest_framework import generics
from .models import Ad, Review, Category
from .serializers import AdSerializer, ReviewSerializer, CategorySerializer

# Список всех объявлений и создание нового объявления
class AdList(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

# Отображение, обновление и удаление конкретного объявления
class AdDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

# Список всех отзывов и создание нового отзыва
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Отображение, обновление и удаление конкретного отзыва
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Список всех категорий и создание новой категории
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Отображение, обновление и удаление конкретной категории
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```

### Описание классов

- **`ListCreateAPIView`**: отображение списка объектов и создание новых.
- **`RetrieveUpdateDestroyAPIView`**: работа с конкретным объектом (чтение, обновление, удаление).

---
## Назначение прав доступа (`permissions`)

Права доступа в Django REST Framework управляют действиями пользователей с объектами. Вы можете использовать встроенные разрешения или создавать свои собственные.

### Пример создания разрешений

```python
from rest_framework import permissions

# Разрешение только для владельца объекта
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Изменение разрешено только владельцу объекта
        return obj.owner == request.user

# Применение разрешений в представлении
class AdDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
```

### Описание встроенных разрешений

- **`IsAuthenticatedOrReadOnly`**: изменения доступны только аутентифицированным пользователям, для остальных разрешено чтение.
- **`IsOwnerOrReadOnly`**: доступ к редактированию объекта только у его владельца.

---
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

---
## Заключение

В данном руководстве представлены ключевые подходы к работе с Django REST Framework:

- Использование классов `generics` для быстрого создания API.
- Настройка разрешений для контроля доступа.
- Тестирование API с помощью **Postman** для обеспечения его функциональности.

Следуя этим инструкциям, вы сможете легко разрабатывать и поддерживать RESTful API для своих проектов.

