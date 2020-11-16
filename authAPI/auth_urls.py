from django.urls import path, include
from .views import *

urlpatterns = [
    path('sign-up', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('update', ChangeProfileView.as_view()),
]