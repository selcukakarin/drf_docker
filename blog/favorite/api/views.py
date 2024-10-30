from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from favorite.api.permissions import IsOwner
from favorite.api.serializers import FavoriteListCreateAPISerializer, FavoriteAPISerializer
from favorite.models import Favorite


class FavoriteListCreateAPIView(ListCreateAPIView):
    # queryset = Favorite.objects.all()
    serializer_class = FavoriteListCreateAPISerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = FavoriteAPISerializer
    queryset = Favorite.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsOwner]


class FavoriteRUDAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = FavoriteAPISerializer
    queryset = Favorite.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsOwner]
