from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet)

router_api = DefaultRouter()
router_api.register('v1/genres', GenreViewSet, basename='genre')
router_api.register('v1/categories', CategoryViewSet, basename='category')
router_api.register('v1/titles', TitleViewSet, basename='title')
router_api.register('v1/users', UserViewSet, basename='users')
router_api.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_api.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router_api.urls)),
]
