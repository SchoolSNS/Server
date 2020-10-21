from django.urls import path, include
from .views import MyProfileView, UserProfileView, UsersPostView, UsersCommentView

urlpatterns = [
    path('', MyProfileView.as_view({'get': 'list'})),
    path('/<int:user_id>', UserProfileView.as_view({'get': 'list'})),
    path('/<int:user_id>/posts', UsersPostView.as_view({'get': 'list'})),
    path('/<int:user_id>/comments', UsersPostView.as_view({'get': 'list'})),
]