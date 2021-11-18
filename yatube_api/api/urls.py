from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

from api.views import (GroupViewSet, UserViewSet,
                       PostViewSet, CommentViewSet)

router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('users', UserViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')
router.register('groups', GroupViewSet)



urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
