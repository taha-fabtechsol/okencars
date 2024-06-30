from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, send_mail
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action

from app import filters, models, serializers, utils, choices, permissions
from app.forms import NewUserForm
from app.token import account_activation_token
from project import settings

import stripe
import json

stripe.api_key = settings.STRIPE


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "password/acc_activated.html")
    else:
        return HttpResponse("Activation link is invalid!")

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user and user.role in [choices.UserRole.DRIVER, choices.UserRole.OWNER]:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"user": serializers.ListUserSerializer(user).data, "token": token.key},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"non_field_errors": ["Unable to log in with provided credentials."]},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(),permissions.HasUserPermission()]
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.ListUserSerializer
        else:
            return super().get_serializer_class()
        
    def get_queryset(self):
        user = self.request.user
        queryset = models.User.objects.all()
        if user.role in [choices.UserRole.MANAGER, choices.UserRole.OWNER]:
            return queryset.filter(owner=user)
        if user.role == choices.UserRole.DRIVER:
            return queryset.filter(id=user.id)
        return queryset

    def create(self, request, *args, **kwargs):
        owner = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.username = request.data["email"]
        user.owner = owner
        utils.send_welcome_mail(user, owner, request.data["password"])
        user.set_password(request.data["password"])
        user.save()
        data = serializers.UserSerializer(
            user,
            context=self.get_serializer_context(),
        ).data
        del data["password"]
        return Response({"user": data}, status=status.HTTP_201_CREATED)
    

class LogoutView(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.none()
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except:
            pass
        logout(request)
        return Response({"status": "User Logged out successfully"})

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VehicleSerializer
    
    @action(detail=False, methods=["post"])
    def checkout(self, request):
        user = request.user
        vehicle = models.Vehicle.objects.filter(id=request.data.get("vehicle")).last()
        date_from = request.data.get("date_from")
        date_to = request.data.get("date_to")
        days = request.data.get("days")
        session = stripe.checkout.Session.create(
            mode="payment",
            customer_email=user.email,
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "USD",
                        "unit_amount": int(vehicle.rent * 100 ) * days,
                        "product_data": {
                            "name": "Car Booking",
                        },
                    },
                    "quantity": 1,
                },
            ],
            metadata={
                "type": "CarRent" ,
                "user": user.id ,
            },
            success_url=f"{settings.FRONTEND_ADDRESS}/success/",
            cancel_url=f"{settings.FRONTEND_ADDRESS}/cancel/",
        )
        return Response({"url":session.url})
        
        
    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.ListVehicleSerializer
        else:
            return super().get_serializer_class()
        
    def get_queryset(self):
        user = self.request.user
        queryset = models.Vehicle.objects.all()
        return queryset
        # if user.role == choices.UserRole.OWNER:
        #     return queryset.filter(owner=user)
        # return queryset.filter(status=choices.VehicleStatus.APPROVED)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        

# class VehicleImageViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.VehicleImagesSerializer
    
#     def get_queryset(self):
#         user = self.request.user
#         queryset = models.VehicleImages.objects.all()
#         return queryset
