from django.utils import timesince, timezone
from rest_framework import serializers

from app import models, choices


def BuildTime(created_at):
    today = timezone.now().date()
    if today == created_at.date():
        date = created_at.time().strftime("%I:%M %p")
    else:
        date = f"{created_at.date()} {created_at.time().strftime('%I:%M %p')}"
    return date


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "first_name",
            "last_name",
            "email",
            "role",
            "dp",
            "password",
            "phone_number",
            "street_address",
            "city",
            "state_province",
            "postal_code",
            "country",
            "date_of_birth",
            "license_number",
            "license_issuing_country",
            "license_expiry_date",
        ]
        
    def get_fields(self):
        fields =  super().get_fields()
        if "request" in self.context.keys() and self.context["request"].method == "PATCH":
            fields.pop("email")
            fields.pop("password")
        return fields
        
    def validate_role(self, val):
        user = self.context["request"].user
        if user.role == choices.UserRole.MANAGER and val not in [choices.UserRole.DRIVER,choices.UserRole.OWNER]:
            raise serializers.ValidationError("You can create only driver and owners.")
        else:
            return val
            
            
class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("password","is_staff", "is_superuser", "groups", "user_permissions")
        model = models.User
        

class ListVehicleSerializer(serializers.ModelSerializer):
    owner = ListUserSerializer()
    class Meta:
        fields = "__all__"
        model = models.Vehicle
                
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("owner",)
        model = models.Vehicle
        
    def validate_availability_dates_from(self, val):
        if val < timezone.now().date():
            raise serializers.ValidationError("Availability should greater than today")
        return val
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["availability_dates_from"] < attrs["availability_dates_to"]:
            raise serializers.ValidationError("Availability date from should be greater than availability date to")
        return attrs