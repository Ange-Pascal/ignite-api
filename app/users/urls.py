from django.urls import path
from . import views
from .views import CustomTokenObtainPairView, ManageUserView
from . import views
from users.views import AddInstructorRoleView
from .views import ProtectedView, AdminOnlyView

app_name = "user"

urlpatterns = [
    path("", views.CreateUserView.as_view(), name="users"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("me/", ManageUserView.as_view(), name="me"),
    path("list-or-self/", views.UserListOrSelfView.as_view(), name="list_or_self"),
    path("delete/<int:id>/", views.UserDeleteView.as_view(), name="user_delete"),
    path("<int:user_id>/add-instructor-role/", AddInstructorRoleView.as_view(), name="add-instructor-role"),
    path("api/protected/", ProtectedView.as_view(), name="protected-view"),
    path("api/admin-only/", AdminOnlyView.as_view(), name="admin-only"),
]
