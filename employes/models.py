from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    company_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Employee(models.Model):

    ROLE_CHOICES = [
        ("COMPANY_HEAD", "Company Head"),
        ("EMPLOYEE", "Employee"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="employees"
    )

    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    joining_date = models.DateField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="EMPLOYEE")

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
