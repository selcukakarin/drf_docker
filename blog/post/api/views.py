from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .paginations import PostPagination
from .permissions import IsOwner
from .serializers import PostSerializer, PostUpdateCreateSerializer
from .throttles import PostListThrottle
from ..models import Post


class PostListAPIView(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    pagination_class = PostPagination
    # throttle_classes = [PostListThrottle]
    throttle_scope = 'turkiye'

    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)
        return queryset

    # beyaz kutu testi : kodların içeriğiyle ilgili ve hatta kodların bağlı olduğu diğer kodlarla ilgili testler
    # siyah kutu testi : kodların içeriğiyle ilgilenmeyip, girdi çıktılarla ilgilenir.





class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]


class PostUpdateAPIView(RetrieveUpdateAPIView, DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        # email gönderme yapabiliriz.
        # zamanlanmış tasklar çalıştırabiliriz.
        serializer.save(modified_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # email gönderme yapabiliriz.
        # zamanlanmış tasklar çalıştırabiliriz.
        serializer.save(user=self.request.user)
