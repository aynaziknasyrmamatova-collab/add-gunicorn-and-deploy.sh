from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

INTRO_TAG = ['Базовый API (Intro)']


class HelloApiView(APIView):
    @extend_schema(
        tags=INTRO_TAG,
        summary='Тестовое приветствие API',
        responses={200: OpenApiResponse(description='Приветственное сообщение')},
    )
    def get(self, request):
        return Response({
            "message": "я Джанго Рест Фреймворк"
        })


class Profile(APIView):
    @extend_schema(
        tags=INTRO_TAG,
        summary='Профиль студента (Урок 1)',
        responses={200: OpenApiResponse(description='Данные автора')},
    )
    def get(self, request):
        return Response({
            "name": "Alisher",
            "age": "19",
            "group": "39-1B"
        })