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
    pass


@admin.register(Transaction)
class EmployeeAdmin(admin.ModelAdmin):
    pass
