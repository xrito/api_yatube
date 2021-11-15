from django.urls import include, path
from rest_framework.routers import SimpleRouter
# from rest_framework.urlpatterns import format_suffix_patterns

from .views import (CommentViewSet, GroupViewSet, UserViewSet,
                    PostViewSet)

# from . import views

router = SimpleRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)
# router.register(r'posts/<int:pk>/comments/', CommentViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('users/', views.UserList.as_view()),
    # path('users/<int:pk>/', views.UserDetail.as_view()),
    # path('api-token-auth/', views.obtain_auth_token),
    # path('posts/', PostViewSet),
    # path('posts/<int:pk>/', PostViewSet),
    # path('groups/', GroupViewSet),
    # path('groups/<int:pk>/', GroupViewSet),
    path('posts/<int:pk>/comments/', CommentViewSet),
    # path('posts/<int:pk>/comments/<int:pk>/', CommentViewSet)
]

# urlpatterns = format_suffix_patterns(urlpatterns)
