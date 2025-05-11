from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from posts.models import Post, Group, Follow
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .serializers import FollowSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.pagination import LimitOffsetPagination


class OptionalPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        if not (request.query_params.get(
            self.limit_query_param) or request.query_params.get(
                self.offset_query_param)):
            return None
        return super().paginate_queryset(queryset, request, view)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'author__username']
    pagination_class = OptionalPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
