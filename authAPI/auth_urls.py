from django.urls import path, include
from .views import *

urlpatterns = [
    path('sign-up', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('update/profile', ChangeProfileView.as_view()),
    path('update/introduce', ChangeIntroduceView.as_view()),
]