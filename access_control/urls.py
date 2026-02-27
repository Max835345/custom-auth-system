from django.urls import path
from .views import CreateRoleView, AssignPermissionToRoleView, AddPermissionToRoleView

urlpatterns = [
    path("admin/roles/", CreateRoleView.as_view()),
    path("admin/assign-permission/", AssignPermissionToRoleView.as_view()),
    path("add-permission/", AddPermissionToRoleView.as_view()),
]