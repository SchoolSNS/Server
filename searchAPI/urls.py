from django.urls import path, include
from .views import SchoolSearchView, UserSearchView

urlpatterns = [
    path('school', SchoolSearchView.as_view()),
    path('user', UserSearchView.as_view()),
]