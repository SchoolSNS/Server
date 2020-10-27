from django.urls import path, include
from .views import SchoolSearchView, UserSearchView, AllUserView

urlpatterns = [
    path('school', SchoolSearchView.as_view()),
    path('search-user', UserSearchView.as_view()),
    path('all-user', AllUserView.as_view()),
]