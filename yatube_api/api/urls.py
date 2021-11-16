from django.urls import include, path
from rest_framework.routers import SimpleRouter

from rest_framework.authtoken import views
from api.views import (GroupViewSet, UserViewSet,
                       PostViewSet, CommentViewSet)

router = SimpleRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)
router.register(
    r'posts/(?P<post_id>[^/.]+)/comments', CommentViewSet, basename='comment')
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
