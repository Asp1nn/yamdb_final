from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitlesFilter
from .models import Category, Genre, Review, Title, User
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrNotSimpleUserReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MyTokenObtainSerializer,
                          ReviewSerializer, TitleSerializerOnePost,
                          TitleSerializerReadOnly, UserAdminSerializer,
                          UserCreateSerializer)
from .utils import (account_activation_token, send_confirmation_code,
                    set_username)


class CreateUserByEmail(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = set_username(email)
        user, _ = User.objects.get_or_create(email=email, username=username)
        user.is_active = False
        user.save()
        confirmation_code = account_activation_token.make_token(user)
        return send_confirmation_code(email, confirmation_code)


class TokenObtain(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MyTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, email=serializer.validated_data['email']
        )
        if not account_activation_token.check_token(
            user, serializer.validated_data['confirmation_code']
        ):
            return Response(
                {
                    'detail':
                        'Неправильный адрес электронной почты'
                        ' или код подтверждения'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken().for_user(user)
        response = {'token': str(token)}
        user.is_active = True
        user.save()
        return Response(response, status=status.HTTP_200_OK)


class UserAdminViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    @action(
        methods=['patch', 'get'], detail=False,
        url_path='me', url_name='me',
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if not self.request.method == 'PATCH':
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewSetWithoutRetrieveAndUpdate(mixins.CreateModelMixin,
                                      mixins.ListModelMixin,
                                      mixins.DestroyModelMixin,
                                      viewsets.GenericViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(ViewSetWithoutRetrieveAndUpdate):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrNotSimpleUserReadOnly
    ]

    def get_queryset(self):
        review = get_object_or_404(
            Review.objects.prefetch_related('comments'),
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrNotSimpleUserReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(
            Title.objects.prefetch_related('reviews'),
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)


class CategoryViewSet(ViewSetWithoutRetrieveAndUpdate):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        actions = ['create', 'partial_update']
        if self.action in actions:
            return TitleSerializerOnePost
        return TitleSerializerReadOnly
