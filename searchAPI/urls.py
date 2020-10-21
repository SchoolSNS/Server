from django.urls import path, include
from .views import SchoolSearchView

urlpatterns = [
    path('school', SchoolSearchView.as_view()),
]