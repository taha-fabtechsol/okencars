from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from app import views

router = routers.DefaultRouter()
router.register(r"user", views.UserViewSet, "user")
router.register(r"vehicle", views.VehicleViewSet, "vehicle")

router.register(r"logout", views.LogoutView, "logout")

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="api_token_auth"),
    path(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.activate,
        name="activate",
    ),
    path("", include(router.urls)),
]
