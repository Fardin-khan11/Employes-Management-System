from django.urls import path
from . import views


urlpatterns = [
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
    "company/employes/",
    views.company_employees,
    name="company_employees"),
     path(
        "employee/profile/",
        views.employee_profile,
        name="employee_profile"),
    path(
    "company/employees/add/",
    views.add_employee,
    name="add_employee"),

    path(
    "company/employees/edit/<int:employee_id>/",
    views.edit_employee,
    name="edit_employee"),

    path(
    "company/employees/delete/<int:employee_id>/",
    views.delete_employee,
    name="delete_employee"),

    path(
    "super-admin/companies/",
    views.super_admin_companies,
    name="super_admin_companies"),

    path(
    "super-admin/companies/add/",
    views.add_company,
    name="add_company"),

    path(
    "super-admin/companies/<int:company_id>/employees/",
    views.super_admin_company_employees,
    name="super_admin_company_employees"),

    path(
    "super-admin/companies/edit/<int:company_id>/",
    views.edit_company,
    name="edit_company"),

    path(
    "super-admin/companies/delete/<int:company_id>/",
    views.delete_company,
    name="delete_company"),

    path(
    "api/companies/",
    views.company_api,
    name="company_api"),

    path(
    "api/employees/",
    views.employee_api,
    name="employee_api"),

    
path(
    "super-admin/employees/<int:employee_id>/edit/",
    views.super_admin_edit_employee,
    name="super_admin_edit_employee",
),

path(
    "super-admin/employees/<int:employee_id>/delete/",
    views.super_admin_delete_employee,
    name="super_admin_delete_employee",
),

path(
    "super-admin/employees/",
    views.super_admin_employees,
    name="super_admin_employees",
),


path(
    "super-admin/employees/add/",
    views.super_admin_add_employee,
    name="super_admin_add_employee",
),


]