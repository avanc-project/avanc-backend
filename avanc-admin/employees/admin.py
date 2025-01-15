from django.contrib import admin

# Register your models here.
from .models import Employee, Employer, SalaryAdvanceRequest, Transaction


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "employer", "salary", "available_amount", "email", "phone")

    list_filter = ("employer",)
    search_fields = ("full_name", "employer")


@admin.register(Employer)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_email",)
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(SalaryAdvanceRequest)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee", "amount_requested",
                    "status", "request_date", "review_date")

    list_filter = ("status", "request_date")

    search_fields = ("employee", "status",)
