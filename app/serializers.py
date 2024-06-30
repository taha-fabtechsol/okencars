from django.utils import timesince, timezone
from rest_framework import serializers

from app import models, choices
from project import settings


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
        
class VehicleImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VehicleImages
        fields = "__all__"
        
class ListVehicleSerializer(serializers.ModelSerializer):
    owner = ListUserSerializer()
    images = serializers.SerializerMethodField()
    status = serializers.CharField(source="get_status_display")
    fuel_type = serializers.CharField(source="get_fuel_type_display")
    transmission_type = serializers.CharField(source="get_transmission_type_display")
    
    def get_images(self, obj):
        return VehicleImagesSerializer(models.VehicleImages.objects.filter(vehicle=obj), many=True, context={'request': self.context["request"]}).data
    class Meta:
        fields = "__all__"
        model = models.Vehicle
                
class VehicleSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField())
    class Meta:
        exclude = ("owner","status")
        model = models.Vehicle
        
    def create(self, validated_data):
        images = validated_data.pop("images")
        vehicle = super().create(validated_data)
        for image in images:
            models.VehicleImages.objects.create(vehicle=vehicle, image=image)
        return vehicle

    def update(self, instance, validated_data):
        images = validated_data.pop("images")
        vehicle = super().update(instance, validated_data)
        for image in images:
            models.VehicleImages.objects.create(vehicle=vehicle, image=image)
        return vehicle

        
        
    def to_representation(self, instance):
        return ListVehicleSerializer(instance, context={'request': self.context["request"]}).data