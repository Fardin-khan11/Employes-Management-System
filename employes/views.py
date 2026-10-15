from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Employee, Company
from .forms import (
    EmployeeForm,
    EditEmployeeForm,
    CompanyForm,
    SuperAdminEmployeeForm,
    SuperAdminEmployeeEditForm,
)
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CompanySerializer, EmployeeSerializer
from django.contrib import messages

# Create your views here.


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):

    # Super Admin
    if request.user.is_superuser:

        total_companies = Company.objects.count()
        total_Employees = Employee.objects.count()

        return render(
            request,
            "super_admin_dashboard.html",
            {
                "total_employees": total_Employees,
            },
        )

    # Company Head / Employee
    employee = request.user.employee

    if employee.role == "COMPANY_HEAD":

        total_employees = (
            Employee.objects.filter(company=employee.company)
            .exclude(user=request.user)
            .count()
        )

        return render(
            request,
            "company_head_dashboard.html",
            {
                "total_employees": total_employees,
                "company": employee.company,
            },
        )

    elif employee.role == "EMPLOYEE":
        return render(request, "employee_dashboard.html", {"employee": employee})

    return render(request, "dashboard.html")


@login_required
def employee_profile(request):

    employee = request.user.employee

    return render(request, "employee_profile.html", {"employee": employee})


@login_required
def company_employees(request):
    if request.user.is_superuser:
        return redirect("super_admin_companies")

    employee = request.user.employee

    # Sirf Company Head ko allow karo
    if employee.role != "COMPANY_HEAD":
        return redirect("dashboard")

    # Sirf uski own company ke employees
    employees = Employee.objects.filter(company=employee.company).exclude(
        user=request.user
    )

    # Search
    search = request.GET.get("search")

    if search:
        employees = (
            employees.filter(employee_id__icontains=search)
            | employees.filter(department__icontains=search)
            | employees.filter(designation__icontains=search)
            | employees.filter(user__first_name__icontains=search)
            | employees.filter(user__last_name__icontains=search)
        )
    paginator = Paginator(employees, 10)

    page_number = request.GET.get("page")

    employees = paginator.get_page(page_number)
    return render(
        request,
        "company_employees.html",
        {
            "employees": employees,
            "company": employee.company,
            "search": search,
        },
    )


@login_required
def add_employee(request):

    employee = request.user.employee

    # Sirf Company Head ko allow karo
    if employee.role != "COMPANY_HEAD":
        return redirect("dashboard")

    if request.method == "POST":

        form = EmployeeForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )

            new_employee = form.save(commit=False)

            new_employee.user = user
            new_employee.company = employee.company
            new_employee.role = "EMPLOYEE"

            new_employee.save()

            messages.success(request, "Employee added successfully!")

        return redirect("company_employees")

    else:
        form = EmployeeForm()

    return render(request, "add_employee.html", {"form": form})


@login_required
def edit_employee(request, employee_id):

    company_head = request.user.employee

    # Sirf Company Head ko allow karo
    if company_head.role != "COMPANY_HEAD":
        return redirect("dashboard")

    # Sirf apni company ka employee mile
    employee = get_object_or_404(Employee, id=employee_id, company=company_head.company)

    if request.method == "POST":

        form = EditEmployeeForm(request.POST, instance=employee)

        if form.is_valid():

            # Employee table update
            form.save()

            # User table update
            user = employee.user

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]

            user.save()

            messages.success(request, "Employee updated successfully!")

            return redirect("company_employees")

    else:
        form = EditEmployeeForm(
            instance=employee,
            initial={
                "first_name": employee.user.first_name,
                "last_name": employee.user.last_name,
            },
        )

    return render(request, "edit_employee.html", {"form": form, "employee": employee})


@login_required
def delete_employee(request, employee_id):

    company_head = request.user.employee

    if company_head.role != "COMPANY_HEAD":
        return redirect("dashboard")

    employee = get_object_or_404(Employee, id=employee_id, company=company_head.company)

    if request.method == "POST":
        employee.delete()

        user.delete()

        messages.success(request, "Employee deleted successfully!")

        return redirect("company_employees")

    return render(request, "delete_employee.html", {"employee": employee})


@login_required
def super_admin_companies(request):

    if not request.user.is_superuser:
        return redirect("dashboard")

    companies = Company.objects.all()

    return render(request, "super_admin_companies.html", {"companies": companies})


@login_required
def super_admin_edit_employee(request, employee_id):
    # Only Super Admin can edit employees
    if not request.user.is_superuser:
        return redirect("dashboard")

    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        form = EditEmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            form.save()

            # Update the linked Django User's name
            user = employee.user
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            messages.success(request, "Employee updated successfully!")
            return redirect(
                "super_admin_company_employees", company_id=employee.company.id
            )
    else:
        form = EditEmployeeForm(
            instance=employee,
            initial={
                "first_name": employee.user.first_name,
                "last_name": employee.user.last_name,
            },
        )

    return render(
        request,
        "edit_employee.html",
        {
            "form": form,
            "employee": employee,
        },
    )


@login_required
def super_admin_delete_employee(request, employee_id):
    # Only Super Admin can delete employees
    if not request.user.is_superuser:
        return redirect("dashboard")

    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        company_id = employee.company.id
        user = employee.user

        employee.delete()
        user.delete()

        messages.success(request, "Employee deleted successfully!")
        return redirect("super_admin_company_employees", company_id=company_id)

    return render(
        request,
        "delete_employee.html",
        {
            "employee": employee,
        },
    )


@login_required
def add_company(request):

    if not request.user.is_superuser:
        return redirect("dashboard")

    if request.method == "POST":

        form = CompanyForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Company added successfully!")

            return redirect("super_admin_companies")

    else:
        form = CompanyForm()

    return render(request, "add_company.html", {"form": form})


@login_required
def super_admin_company_employees(request, company_id):

    if not request.user.is_superuser:
        return redirect("dashboard")

    company = get_object_or_404(Company, id=company_id)

    employees = Employee.objects.filter(company=company)

    return render(
        request,
        "super_admin_company_employees.html",
        {
            "company": company,
            "employees": employees,
        },
    )


@login_required
def edit_company(request, company_id):

    if not request.user.is_superuser:
        return redirect("dashboard")

    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":

        form = CompanyForm(request.POST, instance=company)

        if form.is_valid():
            form.save()

            messages.success(request, "Company updated successfully!")

            return redirect("super_admin_companies")

    else:
        form = CompanyForm(instance=company)

    return render(request, "edit_company.html", {"form": form, "company": company})


@login_required
def delete_company(request, company_id):

    if not request.user.is_superuser:
        return redirect("dashboard")

    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":

        company.delete()

        messages.success(request, "Company deleted successfully!")

        return redirect("super_admin_companies")

    return render(request, "delete_company.html", {"company": company})


@api_view(["GET"])
def company_api(request):

    if not request.user.is_superuser:
        return Response({"error": "Only Super Admin can access this API"}, status=403)

    companies = Company.objects.all()

    serializer = CompanySerializer(companies, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def employee_api(request):

    user = request.user

    # Super Admin
    if user.is_superuser:

        employees = Employee.objects.all()

    else:

        employee = user.employee

        # Company Head
        if employee.role == "COMPANY_HEAD":

            employees = Employee.objects.filter(company=employee.company)

        # Normal Employee
        elif employee.role == "EMPLOYEE":

            employees = Employee.objects.filter(user=user)

        else:

            return Response({"error": "Invalid role"}, status=403)

    serializer = EmployeeSerializer(employees, many=True)

    return Response(serializer.data)


@login_required
def super_admin_employees(request):
    if not request.user.is_superuser:
        return redirect("dashboard")

    employees = (
        Employee.objects.select_related("user", "company")
        .all()
        .order_by("company__name", "employee_id")
    )

    return render(
        request,
        "super_admin_employees.html",
        {"employees": employees},
    )


@login_required
def super_admin_add_employee(request):
    if not request.user.is_superuser:
        return redirect("dashboard")

    if request.method == "POST":
        form = SuperAdminEmployeeForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]

            if User.objects.filter(username=username).exists():
                form.add_error("username", "This username already exists.")
            else:
                user = User.objects.create_user(
                    username=username,
                    password=form.cleaned_data["password"],
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                )

                employee = form.save(commit=False)
                employee.user = user
                employee.save()

                messages.success(request, "Employee added successfully!")
                return redirect("super_admin_employees")
    else:
        form = SuperAdminEmployeeForm()

    return render(
        request,
        "super_admin_add_employee.html",
        {
            "form": form,
        },
    )


@login_required
def super_admin_edit_employee(request, employee_id):
    if not request.user.is_superuser:
        return redirect("dashboard")

    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        form = SuperAdminEmployeeEditForm(request.POST, instance=employee)

        if form.is_valid():
            form.save()

            employee.user.first_name = form.cleaned_data["first_name"]
            employee.user.last_name = form.cleaned_data["last_name"]
            employee.user.save()

            messages.success(request, "Employee updated successfully!")
            return redirect("super_admin_employees")
    else:
        form = SuperAdminEmployeeEditForm(
            instance=employee,
            initial={
                "first_name": employee.user.first_name,
                "last_name": employee.user.last_name,
            },
        )

    return render(
        request,
        "super_admin_edit_employee.html",
        {
            "form": form,
            "employee": employee,
        },
    )


@login_required
def super_admin_delete_employee(request, employee_id):
    if not request.user.is_superuser:
        return redirect("dashboard")

    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        employee.user.delete()
        messages.success(request, "Employee deleted successfully!")
        return redirect("super_admin_employees")

    return render(
        request,
        "super_admin_delete_employee.html",
        {
            "employee": employee,
        },
    )
