from django.contrib import admin

# Register your models here.
from .models import Employee, Employer, SalaryAdvanceRequest, Transaction


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Employer)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(SalaryAdvanceRequest)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee", "amount_requested",
                    "status", "request_date", "review_date")

    list_filter = ("status", "request_date")

    search_fields = ("employee", "status",)
