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
    
    def get(self, request, id=None):
        context = self.context
        if id:
            user = models.User.objects.get(id=id)
            if request.user == user:
                messages.error(request, "Cannot delete your own account.")
            else:
                user.delete()
                return redirect("/back-office/users/")
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
class EditUser(View):
    template_name = "backoffice/edituser.html"
    context = {}
    
    def get(self, request, id):
        context = self.context
        context["obj"] = models.User.objects.get(id=id)
        return render(
            request=request, template_name=self.template_name, context=self.context
        )
        
    def post(self, request, id):
        context = self.context
        try:
            user = models.User.objects.get(id=id)
            keys = list(request.POST.keys())
            for key in keys:
                if request.POST.get(key):
                    if key == "password":
                        user.set_password(request.POST.get(key))
                    else:
                        setattr(user, key, request.POST.get(key))
            user.save()
            if user == request.user:
                login(request, user)
            if "dp" in request.FILES.keys() and request.FILES.get("dp"):
                print("image")
                user.dp = request.FILES.get("dp")
                user.save(update_fields=["dp"])
            messages.success(request, "User updated successfully")
            return redirect(f"/back-office/edit-user/{user.id}/")
        except:
            return render(
                request=request, template_name=self.template_name, context=self.context
            )

    
@method_decorator(login_required, name='dispatch')        
class Vehicle(View):
    template_name = "backoffice/vehicles.html"
    context = {}
    
    def get(self, request, id=None):
        context = self.context
        if id:
            models.Vehicle.objects.get(id=id).delete()
            return redirect("/back-office/vehicles/")
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
        if not "images" in request.FILES.keys() or not request.FILES.getlist("images"):
            messages.error(request ,"Please select atleast 1 file.")
            return render(
                request=request, template_name=self.template_name
            )
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            for image in request.FILES.getlist("images"):
                models.VehicleImages.objects.create(vehicle=vehicle, image=image)
            messages.success(request, "Successfully added the Vehicle.")
            return render(
                request=request, template_name=self.template_name
            )
        else:
            form = form
        return render(
        request=request, template_name=self.template_name, context={'form': form }
    )
    
    
    
@method_decorator(login_required, name='dispatch')
class ModifyVehicle(View):
    template_name = "backoffice/editvehicle.html"
    context = {}
    
    def get(self, request, id):
        context = self.context
        vehicle = models.Vehicle.objects.get(id=id)
        context["vehicle"] = vehicle
        context["images"] = models.VehicleImages.objects.filter(vehicle=vehicle)
        context["vehicle_types"] = choices.Category.choices
        context["transmission_types"] = choices.Transmission.choices
        context["fuel_types"] = choices.Fuel.choices
        return render(
            request=request, template_name=self.template_name, context=self.context
        )
    
    def post(self, request, id):
        context = self.context
        try:
            vehicle = models.Vehicle.objects.get(id=id)
            keys = list(request.POST.keys())
            keys.remove("csrfmiddlewaretoken")
            for key in keys:
                setattr(vehicle, key, request.POST.get(key))
            vehicle.save()
            if "images" in request.FILES.keys():
                models.VehicleImages.objects.create(vehicle=vehicle, image=request.FILES["images"])
            messages.success(request, "Vehicle updated successfully")
            return redirect(f"/back-office/edit-vehicle/{vehicle.id}/")
        except:
            return render(
                request=request, template_name=self.template_name, context=self.context
            )
            
@method_decorator(login_required, name='dispatch')
class ViewVehicle(View):
    template_name = "backoffice/view-vehicle.html"
    context = {}
    
    def get(self, request, id):
        context = self.context
        vehicle = models.Vehicle.objects.get(id=id)
        context["vehicle"] = vehicle
        context["images"] = models.VehicleImages.objects.filter(vehicle=vehicle)
        return render(
            request=request, template_name=self.template_name, context=self.context
        )