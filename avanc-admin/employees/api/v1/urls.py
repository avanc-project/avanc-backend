from django.urls import path

from employees.api.v1 import views

urlpatterns = [
    path('employees/', views.EmployeeListApi.as_view()),
    path('employees/<uuid:pk>', views.EmployeeDetailApi.as_view()),
    path('employees/<uuid:pk>/transactions',
         views.EmployeeTransactionsApi.as_view()),
    path('employees/<uuid:pk>/salary-advances',
         views.EmployeeSalaryAdvanceRequestApi.as_view()),
]
