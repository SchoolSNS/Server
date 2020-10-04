from django.urls import path, include
from .views import registerView, loginView

urlpatterns = [
    path('signUp', registerView.as_view()),
    path('login', loginView.as_view()),
]