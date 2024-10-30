from django.urls import path

from favorite.api.views import FavoriteListCreateAPIView, FavoriteRetrieveDestroyAPIView, FavoriteRUDAPIView

app_name = "favorite"

urlpatterns = [
    path('list-create', FavoriteListCreateAPIView.as_view(), name='list-create'),
    path('delete-retrieve/<pk>', FavoriteRetrieveDestroyAPIView.as_view(), name='delete-retrieve'),
    path('rud/<pk>', FavoriteRUDAPIView.as_view(), name='rud'),
]