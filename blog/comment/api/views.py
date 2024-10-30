from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin, \
    ListModelMixin
from rest_framework.permissions import IsAuthenticated

from comment.api.paginations import CommentPagination
from comment.api.permissions import IsOwner
from comment.api.serializers import CommentCreateSerializer, CommentListSerializer, CommentDeleteUpdateSerializer
from comment.models import Comment
from django.db.models import Q


class CommentCreateAPIView(CreateAPIView, ListModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentListAPIView(ListAPIView, CreateModelMixin):
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.all()
        query = self.request.GET.get("q")
        filter_conditions = Q()
        # select * from comment where and content like '%b%' and content like '%e%' or content like '%ü%'
        if query:
            filter_conditions &= Q(post=query)
        queryset = queryset.filter(filter_conditions)
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDeleteAPIView(DestroyAPIView, UpdateModelMixin, RetrieveModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]

    # def post(self):
    #     print("deneme1")

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CommentUpdateAPIView(UpdateAPIView, RetrieveAPIView, DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
