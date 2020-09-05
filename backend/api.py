from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import generics
from knox.models import AuthToken
from .models import User, Note, Temperature, Weight, BloodPressure, TestResult, MedicalData, Medication, Routine, Doctor, Patient
from .serializers import (UserSerializer, GetUserSerializer, NoteSerializer, TemperatureSerializer,
                          WeightSerializer, BloodPressureSerializer, TestResultSerializer, MedicalDataSerializer,
                          GetMedicalDataSerializer, MedicationSerializer, RoutineSerializer, DoctorSerializer, GetDoctorSerializer,
                          PatientSerializer, GetPatientSerializer, LoginSerializer)
User = get_user_model()


class RegisterUser(generics.GenericAPIView):
    serializer_class = UserSerializer

    @classmethod
    def post(self, request, *args, **kwargs):
        formdata = request.data
        print(formdata)
        serializer = UserSerializer(data=formdata)
        serializer.is_valid(raise_exception=True)
        userStatus = ""
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        returnedUser = GetUserSerializer(user)
        if returnedUser.data["is_MP"]:
            data = {"doctorID": formdata["UserID"],
                    "doctor": returnedUser.data["id"]}
            doctorSerializer = DoctorSerializer(data=data)
            doctorSerializer.is_valid(raise_exception=True)
            doctor = doctorSerializer.save()
            userStatus = GetDoctorSerializer(doctor)
        else:
            medicaldata = GetMedicalDataSerializer(
                data={"user": returnedUser.data["id"]})
            medicaldata.is_valid(raise_exception=True)
            medicalData = medicaldata.save()
            returnedData = MedicalDataSerializer(medicalData)

            data = {"patientID": formdata["UserID"],
                    "patient": returnedUser.data["id"],
                    "medicalData": returnedData.data["id"]
                    }

            patientSerializer = PatientSerializer(data=data)
            patientSerializer.is_valid(raise_exception=True)
            patient = patientSerializer.save()
            userStatus = GetPatientSerializer(patient)

        return Response({"user": returnedUser.data, "userStatus": userStatus.data, "token": token})


class LoginUser(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        returnedUser = GetUserSerializer(user)
        userStatus = ""
        if returnedUser.data["is_MP"]:
            doctor = Doctor.objects.get(doctor=returnedUser.data["id"])
            userStatus = GetDoctorSerializer(doctor)
        else:
            patient = Patient.objects.get(patient=returnedUser.data["id"])
            userStatus = GetPatientSerializer(patient)
        return Response({"user": returnedUser.data, "userStatus": userStatus.data, "token": token})
