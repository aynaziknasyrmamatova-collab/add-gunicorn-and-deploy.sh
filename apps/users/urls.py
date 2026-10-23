from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    TokenLoginView,
    TokenLogoutView,
    JWTLoginView,
    JWTRefreshView,
)

urlpatterns = [
    # Регистрация и профиль
    path('register/', RegisterView.as_view(), name='user-register'),
    path('profile/', ProfileView.as_view(), name='user-profile'),

    # DRF Token Authentication (Заголовок: Authorization: Token <ключ>)
    path('login/token/', TokenLoginView.as_view(), name='token-login'),
    path('logout/token/', TokenLogoutView.as_view(), name='token-logout'),

    # JWT Authentication (Заголовок: Authorization: Bearer <access>)
    path('login/jwt/', JWTLoginView.as_view(), name='jwt-login'),
    path('login/jwt/refresh/', JWTRefreshView.as_view(), name='jwt-refresh'),

    # Django Session Authentication (Куки / Сессия)
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
]
