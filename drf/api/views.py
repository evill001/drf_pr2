from django.contrib.auth.models import User

from rest_framework import generics, permissions, views

from . import serializers
from .models import Post, Comment, Category
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly


# Класс для отображения деталей конкретного пользователя
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()  
    serializer_class = serializers.UserSerializer 

# Класс для отображения списка всех постов и создания новых постов
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()  
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Метод для создания нового поста, устанавливает владельца поста
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Класс для отображения, обновления и удаления конкретного поста
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()  
    serializer_class = PostSerializer  
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,  IsOwnerOrReadOnly] 

# Класс для отображения списка всех комментариев и создания новых комментариев
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Метод для создания нового комментария, устанавливает владельца комментария
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Класс для отображения, обновления и удаления конкретного комментария
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] 

# Класс для отображения списка всех категорий и создания новых категорий
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Класс для отображения, обновления и удаления конкретной категории
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
