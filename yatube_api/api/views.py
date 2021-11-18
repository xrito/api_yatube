from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post, User
from .serializers import (CommentSerializer, GroupSerializer, PostSerializer,
                          UserSerializer)
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        post_id = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        new_queryset = post_id.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post_id = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post_id)
