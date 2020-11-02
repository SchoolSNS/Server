from django.urls import path, include
from .views import SchoolSearchView, UserSearchView, AllUserView, PostSearchView

urlpatterns = [
    path('school', SchoolSearchView.as_view()),
    path('search-user', UserSearchView.as_view()),
    path('all-user', AllUserView.as_view()),
    path('post', PostSearchView.as_view()),
]