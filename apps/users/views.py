from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .tokens import token_payload, jwt_payload, user_payload

USER_TAG = ['Пользователи (Users)']


class RegisterView(APIView):
    """
    Регистрация нового пользователя.
    Доступ открыт всем.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(
        tags=USER_TAG,
        summary='Регистрация пользователя',
        description='Регистрирует нового пользователя и возвращает данные профиля с токенами.',
        request=RegisterSerializer,
        responses={201: OpenApiResponse(description='Пользователь зарегистрирован')},
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Пользователь успешно зарегистрирован!",
                "user": user_payload(user),
                "tokens": {
                    "token": token_payload(user)["token"],
                    "jwt": jwt_payload(user),
                }
            },
            status=status.HTTP_201_CREATED
        )


class TokenLoginView(APIView):
    """
    Авторизация через DRF Token (ключ сохраняется в таблице authtoken_token).
    Заголовок для запросов: Authorization: Token <ключ>
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        tags=USER_TAG,
        summary='Вход через DRF Token',
        description='Принимает логин и пароль, возвращает static-токен DRF для заголовка Authorization: Token <ключ>.',
        request=LoginSerializer,
        responses={200: OpenApiResponse(description='Успешная авторизация по токену')},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(token_payload(user), status=status.HTTP_200_OK)


class TokenLogoutView(APIView):
    """
    Выход и удаление DRF Token из базы данных.
    Доступен только авторизованным пользователям.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=USER_TAG,
        summary='Выход (удаление DRF Token)',
        description='Удаляет текущий токен пользователя из БД, аннулируя авторизацию.',
        request=None,
        responses={200: OpenApiResponse(description='Токен удален')},
    )
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(
            {"message": "Токен успешно удален из базы данных."},
            status=status.HTTP_200_OK
        )


class JWTLoginView(APIView):
    """
    Авторизация через SimpleJWT (генерация access и refresh токенов).
    Заголовок для запросов: Authorization: Bearer <access_токен>
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        tags=USER_TAG,
        summary='Вход через JWT (получение access и refresh)',
        description='Принимает логин и пароль, возвращает пару JWT токенов (access + refresh).',
        request=LoginSerializer,
        responses={200: OpenApiResponse(description='Пара JWT токенов')},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(jwt_payload(user), status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        tags=USER_TAG,
        summary='Обновление JWT access токена',
        description='Принимает refresh токен и возвращает свежий access токен.',
        request=TokenRefreshSerializer,
        responses={200: OpenApiResponse(description='Новый access токен')},
    )
)
class JWTRefreshView(TokenRefreshView):
    """
    Эндпоинт для обновления истекшего access токена по refresh токену.
    """
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    """
    Авторизация через классическую сессию Django (SessionAuthentication).
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        tags=USER_TAG,
        summary='Вход через сессию Django (Session)',
        description='Вход в сессию браузера по логину и паролю.',
        request=LoginSerializer,
        responses={200: OpenApiResponse(description='Сессия открыта')},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(
            {
                "message": f"Добро пожаловать, {user.username}!",
                "user": user_payload(user)
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    """
    Выход из сессии Django.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=USER_TAG,
        summary='Выход из сессии Django (Session)',
        description='Завершает активную сессию пользователя.',
        request=None,
        responses={200: OpenApiResponse(description='Сессия завершена')},
    )
    def post(self, request):
        logout(request)
        return Response(
            {"message": "Вы успешно вышли из системы."},
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):
    """
    Просмотр и обновление профиля текущего пользователя (работает с любым способом аутентификации).
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @extend_schema(
        tags=USER_TAG,
        summary='Просмотр профиля текущего пользователя',
        responses={200: UserSerializer},
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=USER_TAG,
        summary='Частичное редактирование своего профиля',
        request=UserSerializer,
        responses={200: UserSerializer},
    )
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
