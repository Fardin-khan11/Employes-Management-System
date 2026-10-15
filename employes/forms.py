from django import forms
from django.contrib.auth.models import User
from .models import Employee, Company


class EmployeeForm(forms.ModelForm):

    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)

    def clean_username(self):

        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        return username

    class Meta:
        model = Employee
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "employee_id",
            "department",
            "designation",
            "joining_date",
        ]
        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"}),
        }


class EditEmployeeForm(forms.ModelForm):

    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "employee_id",
            "department",
            "designation",
            "joining_date",
        ]

        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"}),
        }


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            "name",
            "company_code",
        ]

class SuperAdminEmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = Employee
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "company",
            "employee_id",
            "department",
            "designation",
            "joining_date",
            "role",
        ]
        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"}),
        }

class SuperAdminEmployeeEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "company",
            "employee_id",
            "department",
            "designation",
            "joining_date",
            "role",
        ]
        widgets = {
            "joining_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }
