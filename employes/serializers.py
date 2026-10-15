from rest_framework import serializers
from .models import Company, Employee


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "company_code",
            "created_at",
        ]


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "department",
            "designation",
            "joining_date",
            "role",
            "company",
        ]