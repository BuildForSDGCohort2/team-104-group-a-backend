from .models import User, Note, Temperature, Weight, BloodPressure, TestResult, MedicalData, Medication, Routine, Doctor, Patient
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "UserID", "first_name", "last_name", "gender", "date_of_birth",
                  "email", "phone_number", "address", "image", "licenseNumber", "is_MP", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data["email"], UserID=validated_data["UserID"], first_name=validated_data["first_name"],
                                        last_name=validated_data["last_name"], gender=validated_data[
                                            "gender"], date_of_birth=validated_data["date_of_birth"],
                                        image=validated_data["image"], phone_number=validated_data["phone_number"], address=validated_data["address"], is_MP=validated_data["is_MP"], password=validated_data["password"])
        user.save()
        return user


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "last_login", "is_active", "is_admin",
                   "staff", "is_superuser", "groups", "user_permissions"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Credentials")


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"


class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"


class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = "__all__"


class BloodPressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodPressure
        fields = "__all__"


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = "__all__"


class GetMedicalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalData
        fields = ["user"]


class MedicalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalData
        fields = "__all__"


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = "__all__"


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ["patients"]


class GetDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["patientID", "patient", "medicalData"]


class GetPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
