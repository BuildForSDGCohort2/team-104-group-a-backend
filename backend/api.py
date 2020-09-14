from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from knox.models import AuthToken
from .models import Note, Temperature, Weight, BloodPressure, TestResult, MedicalData, Medication, Routine, Doctor, Patient
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
        serializer = UserSerializer(data=formdata)
        serializer.is_valid(raise_exception=True)
        userStatus = ""
        doctorOrPatient = "patient"
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
            doctorOrPatient = "doctor"
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

        return Response({"user": returnedUser.data, doctorOrPatient: userStatus.data, "token": token})


class LoginUser(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @classmethod
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        returnedUser = GetUserSerializer(user)
        userStatus = ""
        doctorOrPatient = "patient"
        if returnedUser.data["is_MP"]:
            doctorOrPatient = "doctor"
            doctor = Doctor.objects.get(doctor=returnedUser.data["id"])
            userStatus = GetDoctorSerializer(doctor)
        else:
            patient = Patient.objects.get(patient=returnedUser.data["id"])
            userStatus = GetPatientSerializer(patient)
        return Response({"user": returnedUser.data, doctorOrPatient: userStatus.data, "token": token})


class AddMedicalData(generics.GenericAPIView):
    serializer_class = MedicalDataSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    @classmethod
    def post(self, request, *args, **kwargs):
        action = request.data["action"]
        patientMedicalData = MedicalData.objects.get(
            id=int(request.data["medicalData"]))

        if action == "temperature":
            temp = Temperature(
                temperature=request.data["data"]["temperature"])
            temp.save()
            patientMedicalData.temperature.add(temp)
            usertemp = patientMedicalData.temperature
            temperature = TemperatureSerializer(usertemp, many=True)
            return Response({"temperature": temperature.data})
        elif action == "weight":
            weight = Weight(
                weight=request.data["data"]["weight"])
            weight.save()
            patientMedicalData.weight.add(weight)
            userweight = patientMedicalData.weight
            weights = WeightSerializer(userweight, many=True)
            return Response({"weight": weights.data})
        elif action == "bloodPressure":
            bloodPressure = BloodPressure(
                bloodPressure=request.data["data"]["bloodPressure"])
            bloodPressure.save()
            patientMedicalData.bloodPressure.add(bloodPressure)
            userbloodPressure = patientMedicalData.bloodPressure
            bloodPressures = BloodPressureSerializer(
                userbloodPressure, many=True)
            return Response({"bloodPressure": bloodPressures.data})
        elif action == "testResult":
            testResult = TestResult(
                testResult=request.data["data"]["testResult"])
            testResult.save()
            patientMedicalData.testResult.add(testResult)
            usertestResult = patientMedicalData.testResult
            testResults = TestResultSerializer(
                usertestResult, many=True)
            return Response({"testResult": testResults.data})


class SearchAddAndRemoveDoctor(generics.GenericAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    @classmethod
    def post(self, request, *args, **kwargs):
        action = request.data["action"]
        data = request.data["doctorID"]

        if action == "search":
            doctors = Doctor.objects.filter(doctorID=data)
            returnedData = DoctorSerializer(doctors, many=True)
            return Response({"doctors": returnedData.data})
        elif action == "add":
            doctor = Doctor.objects.get(doctorID=data)
            doctor.patients.add(request.user)
            patient = Patient.objects.get(patient=request.user.id)
            patient.aproved.add(doctor)
            returnedData = GetPatientSerializer(patient)
            docs = User.objects.filter(doctor__aproved=patient.id)
            aproved = GetUserSerializer(docs, many=True)
            return Response({"patient": returnedData.data, "aproved": aproved.data})
        elif action == "remove":
            doctor = Doctor.objects.get(doctorID=data)
            doctor.patients.remove(request.user)
            patient = Patient.objects.get(patient=request.user.id)
            patient.aproved.remove(doctor)
            returnedData = GetPatientSerializer(patient)
            docs = User.objects.filter(doctor__aproved=patient.id)
            aproved = GetUserSerializer(docs, many=True)
            return Response({"patient": returnedData.data, "aproved": aproved.data})
