from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from employees.api.v1 import views
from employees.api.v1.views import SignUpApi, SignInApi

urlpatterns = [
    path('employees/', csrf_exempt(views.EmployeeListApi.as_view())),
    path('employees/<uuid:pk>', csrf_exempt(views.EmployeeDetailApi.as_view())),
    path('employees/<uuid:pk>/transactions',
         csrf_exempt(views.EmployeeTransactionsApi.as_view())),
    path('employees/<uuid:pk>/salary-advances',
         csrf_exempt(views.EmployeeSalaryAdvanceRequestApi.as_view())),
    path('signup/', csrf_exempt(SignUpApi.as_view()), name='signup'),
    path('signin/', csrf_exempt(SignInApi.as_view()), name='signin'),
]
