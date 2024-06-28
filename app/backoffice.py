from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.http import response
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .token import account_activation_token
from django.utils import timezone
from django.utils.decorators import method_decorator
from project import settings
import os, re
from django.db.models import Q
from django.utils import timezone
from app import forms, choices, models


class LoginRequest(View):
    template_name = "backoffice/login.html"
    context = {}

    def get(self, request):
        context = self.context
        form = AuthenticationForm()
        context["login_form"] = form
        return render(
            request=request, template_name=self.template_name, context=context
        )

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active == True:
                    if user.role == choices.UserRole.ADMIN:
                        login(request, user)
                        return redirect("/back-office/dashboard/")
                    if user.role == choices.UserRole.MANAGER:
                        login(request, user)
                        return redirect("/back-office/dashboard/")
                else:
                    messages.error(request, "Your account is not active.")
        else:
            if models.User.objects.filter(username=request.POST["username"]).exists():
                messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        context = self.context
        context["login_form"] = form
        return render(
            request=request, template_name=self.template_name, context=context
        )


class logout_request(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("/back-office/login/")
@method_decorator(login_required, name='dispatch')
class Dashboard(View):
    template_name = "backoffice/dashboard.html"
    context = {}
    
    def get(self, request):
        context = self.context
        return render(
            request=request, template_name=self.template_name, context=context
        )
        
@method_decorator(login_required, name='dispatch')
class User(View):
    template_name = "backoffice/users.html"
    context = {}
    
    def get(self, request):
        context = self.context
        user = models.User.objects.all().exclude(id=request.user.id)
        if request.user.role == choices.UserRole.MANAGER:
            user = user.filter(owner=request.user)
        context["users"] = user
        return render(
            request=request, template_name=self.template_name, context=context
        )
        
@method_decorator(login_required, name='dispatch')        
class AddUser(View):
    template_name = "backoffice/adduser.html"
    context = {}
    
    def get(self, request):
        return render(
            request=request, template_name=self.template_name
        )
        
    def post(self, request):
        form = forms.NewUserForm(request.POST, request.FILES)
        if models.User.objects.filter(email=request.POST["email"]).exists():
            messages.error(request, "User with this email is already exists!")
            return render(request=request, template_name=self.template_name)
        if form.is_valid():
            user = form.save()
            user.owner = request.user
            user.username = user.email
            user.save()
            return redirect('/back-office/users/')
        else:
            form = forms.NewUserForm()

        return render(request=request, template_name=self.template_name, context={'form': form })

@method_decorator(login_required, name='dispatch')        
class Vehicle(View):
    template_name = "backoffice/vehicles.html"
    context = {}
    
    def get(self, request):
        context = self.context
        vehicles = models.Vehicle.objects.all()
        if request.user.role == choices.UserRole.MANAGER:
            vehicles = vehicles.filter(owner=request.user)
        context["vehicles"] = vehicles
        return render(
            request=request, template_name=self.template_name, context=context
        )
        
class RedirectView(View):
    def get(self, request):
        return redirect("/back-office/login/")
@method_decorator(login_required, name='dispatch')
class AddVehicle(View):
    template_name = "backoffice/addvehicle.html"
    context = {}
    
    def get(self, request):
        return render(
            request=request, template_name=self.template_name
        )
    
    def post(self, request):
        form = forms.VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, "Successfully added the Vehicle.")
            return render(
                request=request, template_name=self.template_name
            )
        else:
            form = form
        return render(
        request=request, template_name=self.template_name, context={'form': form }
    )
    
            