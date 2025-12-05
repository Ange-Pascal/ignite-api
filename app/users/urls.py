from django.urls import path
from . import views
from .views import CustomTokenObtainPairView, ManageUserView
from . import views

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("me/", ManageUserView.as_view(), name="me"),
    path("list-or-self/", views.UserListOrSelfView.as_view(), name="list_or_self"),
    path("delete/<int:id>/", views.UserDeleteView.as_view(), name="user_delete"),
]
