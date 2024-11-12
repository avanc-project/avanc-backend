from django.urls import path, include


urlpatterns = [
    path('v1/', include('employees.api.v1.urls')),
]
