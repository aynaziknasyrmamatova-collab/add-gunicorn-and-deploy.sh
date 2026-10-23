from django.urls import path

from .views import HelloApiView, Profile

urlpatterns = [
    path('hello/', HelloApiView.as_view()),
    path('profile/', Profile.as_view())
]
