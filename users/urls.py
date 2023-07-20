from django.urls import path
from users.views import UsersView, LoginView, UserDetailView

urlpatterns = [
    path("users/", UsersView.as_view()),
    path("users/login/", LoginView.as_view()),
    path("users/<int:user_id>/", UserDetailView.as_view()),
]
