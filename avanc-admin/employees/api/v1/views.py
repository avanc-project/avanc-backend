from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import QuerySet, Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.contrib.auth.hashers import make_password, check_password
from django.middleware.csrf import get_token

from employees.models import Employee, SalaryAdvanceRequest, Transaction, Employer


class EmployeeListApi(View):
    http_method_names = ['get', 'post', 'put']

    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        data = list(employees.values("id", "full_name", "employer"))
        return JsonResponse({"results": data})

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            employee = Employee.objects.create(**data)
            return JsonResponse({"id": employee.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @method_decorator(csrf_exempt)
    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            for item in data:
                employee_id = item.get('id')
                if not employee_id:
                    continue
                try:
                    employee = Employee.objects.get(pk=employee_id)
                    for key, value in item.items():
                        setattr(employee, key, value)
                    employee.save()
                except Employee.DoesNotExist:
                    continue
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class EmployeeDetailApi(View):
    http_method_names = ['get', 'post', 'put']

    def get(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        try:
            employee = Employee.objects.get(pk=employee_id)
            data = {
                "id": employee.id,
                "full_name": employee.full_name,
                "salary": employee.salary,
                # ...other fields...
            }
            return JsonResponse(data)
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            employee = Employee.objects.create(**data)
            return JsonResponse({"id": employee.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @method_decorator(csrf_exempt)
    def put(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        try:
            employee = Employee.objects.get(pk=employee_id)
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(employee, key, value)
            employee.save()
            return JsonResponse({"id": employee.id})
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get_transactions(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        try:
            employee = Employee.objects.get(pk=employee_id)
            transactions = employee.get_all_transactions()
            data = list(transactions.values(
                "id", "amount", "transaction_date"))
            return JsonResponse({"transactions": data})
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)


class EmployeeTransactionsApi(View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        try:
            employee = Employee.objects.get(pk=employee_id)
            transactions = employee.get_all_transactions()
            data = list(transactions.values(
                "id", "amount", "transaction_date"))
            return JsonResponse({"transactions": data})
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        try:
            employee = Employee.objects.get(pk=employee_id)
            data = json.loads(request.body)
            request_id = data.get('request_id')
            amount = data.get('amount')
            if not request_id or not amount:
                return JsonResponse({"error": "Invalid data"}, status=400)
            salary_request = SalaryAdvanceRequest.objects.get(
                pk=request_id, employee=employee)
            transaction = Transaction.objects.create(
                request=salary_request, amount=amount)
            return JsonResponse({"id": transaction.id}, status=201)
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)
        except SalaryAdvanceRequest.DoesNotExist:
            return JsonResponse({"error": "Salary advance request not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class EmployeeSalaryAdvanceRequestApi(View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        try:
            employee = Employee.objects.get(pk=employee_id)
            requests = SalaryAdvanceRequest.objects.filter(employee=employee)
            data = list(requests.values("id", "amount_requested",
                        "status", "request_date", "review_date"))
            return JsonResponse({"salary_advance_requests": data})
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        try:
            employee = Employee.objects.get(pk=employee_id)
            data = json.loads(request.body)
            amount_requested = data.get('amount_requested')
            if not amount_requested:
                return JsonResponse({"error": "Invalid data"}, status=400)
            salary_request = SalaryAdvanceRequest.objects.create(
                employee=employee, amount_requested=amount_requested)
            return JsonResponse({"id": salary_request.id}, status=201)
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Employee not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class SignUpApi(View):
    http_method_names = ['post']

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            full_name = data.get('full_name')
            salary = data.get('salary')
            employer_name = data.get('employer_name')
            if not email or not password or not full_name or salary is None or not employer_name:
                return JsonResponse({"error": "Invalid data"}, status=400)
            hashed_password = make_password(password)
            employer = Employer.objects.get(name=employer_name)
            employee = Employee.objects.create(
                email=email, password=hashed_password, full_name=full_name, salary=salary, employer=employer)
            return JsonResponse({"id": employee.id, "email": employee.email}, status=201)
        except Employer.DoesNotExist:
            return JsonResponse({"error": "Employer not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class SignInApi(View):
    http_method_names = ['post']

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            if not email or not password:
                return JsonResponse({"error": "Invalid data"}, status=400)
            try:
                employee = Employee.objects.get(email=email)
                print(password == employee.password)
                print(password)
                print(employee.password)

                if check_password(password, employee.password):
                    token = get_token(request)
                    return JsonResponse({"token": token}, status=200)
                else:
                    return JsonResponse({"error": "Invalid credentials"}, status=401)
            except Employee.DoesNotExist:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
