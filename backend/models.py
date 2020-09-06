from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import datetime
from PIL import Image
from math import floor
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, UserID, first_name, last_name, gender, date_of_birth, image,
                    phone_number='null', address="null", licenseNumber="null", is_MP=False, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), UserID=UserID, first_name=first_name, last_name=last_name, gender=gender,
                          date_of_birth=date_of_birth, phone_number=phone_number, image=image, address=address, licenseNumber=licenseNumber, is_MP=is_MP)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password, UserID="null", first_name="TEAM", last_name="LEAD", gender="null",
                                date_of_birth=datetime.date(1994, 11, 25), phone_number="null", address="null", licenseNumber="null", image=None)
        user.is_admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    UserID = models.CharField(verbose_name='user ID', max_length=100)
    first_name = models.CharField(verbose_name='first name', max_length=255)
    last_name = models.CharField(verbose_name='last name', max_length=255)
    gender = models.CharField(verbose_name='gender', max_length=6)
    date_of_birth = models.DateField(
        "date of birth", auto_now=False, auto_now_add=False)
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True,)
    phone_number = models.CharField(verbose_name='phone number', max_length=30)
    address = models.CharField(
        verbose_name='address', max_length=255, default="null")
    # remeber to link a default image
    image = models.ImageField(null=True, default="image not uploaded")
    licenseNumber = models.CharField(
        verbose_name="License number", max_length=150, default='null')
    is_MP = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        if not self.is_admin and self.staff:
            if perm == "backend.add_user" or perm == "backend.change_user" or perm == "backend.delete_user":
                return False
            else:
                return True
        else:
            return True

    def has_module_perms(self, app_label):
        if not self.is_admin and self.staff:
            if app_label == "knox" or app_label == "auth":
                return False
            else:
                return True
        else:
            return True

    @property
    def is_staff(self):
        return self.staff

    def save(self, *args, **kwargs):

        if self.image:
            im = Image.open(self.image)
            width, height = im.size
            output = BytesIO()
            n = 0.5
            Width = floor(width * n)
            Height = floor(height * n)
            if width > 1000:
                im = im.resize((Width, Height))
                im.save(output, format='JPEG', quality=100)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split(
                    '.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super().save(*args, **kwargs)


@receiver(pre_save, sender=User)
def delete_User_image(sender, instance, *args, **kwargs):
    if instance.pk:
        user = User.objects.get(pk=instance.pk)
        if user.image != instance.image:
            user.image.delete(False)


@receiver(post_delete, sender=User)
def delete_User_Image(sender, instance, using, *args, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


class Doctor(models.Model):
    doctorID = models.CharField(verbose_name='user ID', max_length=100)
    doctor = models.ForeignKey(
        User, related_name='doctor', on_delete=models.CASCADE)
    patients = models.ManyToManyField(
        User, related_name='patients', verbose_name="patients")

    def __str__(self):
        return self.doctorID

    class Meta:
        managed = True
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'


class Note(models.Model):
    title = models.CharField(verbose_name="title", max_length=150)
    text = models.CharField(verbose_name="text", max_length=150)
    sender = models.ManyToManyField(Doctor, verbose_name="sender")

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'


class Temperature(models.Model):
    temperature = models.CharField(verbose_name="temperature", max_length=50)

    def __str__(self):
        return self.temperature

    class Meta:
        managed = True
        verbose_name = 'Temperature'
        verbose_name_plural = 'Temperatures'


class Weight(models.Model):
    weight = models.CharField(verbose_name="weight", max_length=50)

    def __str__(self):
        return self.weight

    class Meta:
        managed = True
        verbose_name = 'Weight'
        verbose_name_plural = 'Weights'


class BloodPressure(models.Model):
    bloodPressure = models.CharField(
        verbose_name="blood pressure", max_length=50)

    def __str__(self):
        return self.bloodPressure

    class Meta:
        managed = True
        verbose_name = 'BloodPressure'
        verbose_name_plural = 'BloodPressures'


class TestResult(models.Model):
    testResult = models.ImageField()

    def __str__(self):
        return str(self.testResult)

    class Meta:
        managed = True
        verbose_name = 'TestResult'
        verbose_name_plural = 'TestResults'

#     def save(self, *args, **kwargs):

#         if self.testResult:
#             im = Image.open(self.image)
#             width, height = im.size
#             output = BytesIO()
#             n = 0.5
#             Width = floor(width * n)
#             Height = floor(height * n)
#             if width > 1000:
#                 im = im.resize((Width, Height))
#                 im.save(output, format='JPEG', quality=100)
#                 output.seek(0)
#                 self.testResult = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.testResult.name.split(
#                     '.')[0], 'image/jpeg', sys.getsizeof(output), None)

#         super().save(*args, **kwargs)


# @receiver(pre_save, sender=TestResult)
# def delete_TestResult_image(sender, instance, *args, **kwargs):
#     if instance.pk:
#         testResult = TestResult.objects.get(pk=instance.pk)
#         if testResult.testResult != instance.testResult:
#             testResult.testResult.delete(False)


# @receiver(post_delete, sender=TestResult)
# def delete_TestResult_Image(sender, instance, using, *args, **kwargs):
#     if instance.testResult:
#         instance.testResult.delete(save=False)


class MedicalData(models.Model):
    user = models.ForeignKey(User, verbose_name="user",
                             on_delete=models.CASCADE)
    temperature = models.ManyToManyField(
        Temperature, verbose_name="temperature")
    weight = models.ManyToManyField(Weight, verbose_name="weight")
    bloodPressure = models.ManyToManyField(
        BloodPressure, verbose_name="blood pressure")
    testResult = models.ManyToManyField(TestResult, verbose_name="test result")

    def __str__(self):
        return str(self.user)

    class Meta:
        managed = True
        verbose_name = 'MedicalData'
        verbose_name_plural = 'MedicalDatas'


class Medication(models.Model):
    medicineName = models.CharField(
        verbose_name="medicine name", max_length=150)
    dosagePerIntake = models.IntegerField(verbose_name="dosage per intake")
    timesPerDay = models.IntegerField(verbose_name="times per day")
    hoursIntervalsPerDay = models.IntegerField(
        verbose_name="hours intervals per day")
    totaldosage = models.IntegerField(verbose_name="total dosage")

    def __str__(self):
        return self.medicineName

    class Meta:
        managed = True
        verbose_name = 'Medication'
        verbose_name_plural = 'Medications'


class Routine(models.Model):
    routine = models.CharField(verbose_name="routine", max_length=150)
    start = models.TimeField(verbose_name="start",
                             auto_now=False, auto_now_add=False)
    end = models.TimeField(
        verbose_name="end", auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.routine

    class Meta:

        managed = True
        verbose_name = 'Routine'
        verbose_name_plural = 'Routines'


class Patient(models.Model):
    patientID = models.CharField(verbose_name='user ID', max_length=100)
    patient = models.ForeignKey(
        User, related_name='patient', on_delete=models.CASCADE)
    aproved = models.ManyToManyField(Doctor, verbose_name="patients")
    medicalData = models.ForeignKey(
        MedicalData, related_name='medicaldata', on_delete=models.CASCADE)
    medication = models.ManyToManyField(Medication, verbose_name="patients")
    notes = models.ManyToManyField(Note, verbose_name="notes")

    def __str__(self):
        return str(self.patientID)

    class Meta:
        managed = True
        verbose_name = 'patient'
        verbose_name_plural = 'patients'
