from django.urls import path
from .views import LoginView, RegisterView, LogoutView, UpdateUserView, DeleteUserView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("update/", UpdateUserView.as_view()),
    path("delete/", DeleteUserView.as_view()),
]