from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from app import views, backoffice

router = routers.DefaultRouter()
router.register(r"user", views.UserViewSet, "user")
router.register(r"vehicle", views.VehicleViewSet, "vehicle")
# router.register(r"vehicle-imges", views.VehicleImageViewSet, "vehicle-imges")

router.register(r"logout", views.LogoutView, "logout")

frontofficeurl = router.urls + [
    path("login/", views.LoginView.as_view(), name="api_token_auth"),
]



backofficeurl = [
    path("login/", backoffice.LoginRequest.as_view(), name="login"),
    path("logout/", backoffice.logout_request.as_view(), name="logout"),    
    path("dashboard/", backoffice.Dashboard.as_view(), name="dashboard"),
    path("users/", backoffice.User.as_view(), name="users"),
    path("users/<int:id>/", backoffice.User.as_view(), name="users"),
    path("add-user/", backoffice.AddUser.as_view(), name="add-user"),
    path("edit-user/<int:id>/", backoffice.EditUser.as_view(), name="edit-user"),
    path("vehicles/", backoffice.Vehicle.as_view(), name="vehicles"),
    path("vehicles/<int:id>/", backoffice.Vehicle.as_view(), name="vehicles"),
    path("add-vehicle/", backoffice.AddVehicle.as_view(), name="add-vehicle"),
    path("edit-vehicle/<int:id>/", backoffice.ModifyVehicle.as_view(), name="edit-vehicle"),
    path("view-vehicle/<int:id>/", backoffice.ViewVehicle.as_view(), name="view-vehicle"),
    
]


urlpatterns = [
    path("", backoffice.RedirectView.as_view(), name="login"),
    path(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.activate,
        name="activate",
    ),
    path("api/", include(frontofficeurl)),
    path("back-office/", include(backofficeurl)),
]

