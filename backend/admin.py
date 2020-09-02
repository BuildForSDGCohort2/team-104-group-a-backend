from django.contrib import admin
from django.contrib.auth import get_user_model
Users=get_user_model()
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User,Note,Temperature,Weight,BloodPressure,TestResult,MedicalData,Medication,Routine,Doctor,Patient
from .form import ProductForm

# Register your models here.

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email',)
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

def make_manager(modeladmin, request, querryset):
    for querry in querryset:
        user= querry 
        user.staff=True
        user.save()
        
make_manager.allowed_permissions=("add",)
make_manager.short_description = "make manager(s)"

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin','is_staff')
    list_filter = ('is_admin',)
    actions = [make_manager]
    fieldsets = (
    (None, {'fields': ('UserID','first_name','last_name','gender','date_of_birth','email','phone_number','address','image','is_MP','password')}),
    ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('UserID','first_name','last_name','gender','date_of_birth','email','phone_number','address','image','is_MP','password1', 'password2')}
    ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    
admin.site.register(User,UserAdmin)
admin.site.register(Note)
admin.site.register(Temperature)
admin.site.register(Weight)
admin.site.register(BloodPressure)
admin.site.register(TestResult)
admin.site.register(MedicalData)
admin.site.register(Medication)
admin.site.register(Routine)
admin.site.register(Doctor)
admin.site.register(Patient)