from django.urls import include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet
from .views import CommentViewSet
from .views import CreateUserByEmail
from .views import GenreViewSet
from .views import ReviewViewSet
from .views import TitleViewSet
from .views import TokenObtain
from .views import UserAdminViewSet

router_1 = DefaultRouter()

router_1.register(
    'users',
    UserAdminViewSet,
    basename='users'
)
router_1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


auth_urlpatterns = [
    path(
        'email/',
        CreateUserByEmail.as_view(),
        name='get_conf_code'
    ),
    path(
        'token/',
        csrf_exempt(TokenObtain.as_view()),
        name='token_obtain'
    ),
]


urlpatterns = [
    path(
        'v1/',
        include(router_1.urls)
    ),
    path(
        'v1/auth/',
        include(auth_urlpatterns)
    ),
]
