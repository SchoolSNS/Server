from django.urls import path, include
from .views import RegisterView, LoginView

urlpatterns = [
    path('sign-up', RegisterView.as_view()),
    path('login', LoginView.as_view()),
]