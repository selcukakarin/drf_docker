from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostUpdateAPIView,
    PostCreateAPIView
)

app_name = "post"

urlpatterns = [
    path('list', cache_page(60*1)(PostListAPIView.as_view()), name='post'),
    path('detail/<slug>', PostDetailAPIView.as_view(), name='detail'),
    path('delete/<slug>', PostDeleteAPIView.as_view(), name='delete'),
    path('update/<slug>', PostUpdateAPIView.as_view(), name='update'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
]
