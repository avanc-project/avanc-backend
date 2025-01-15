import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from decimal import Decimal

class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Employer(TimeStampedMixin, UUIDMixin):
    name = models.CharField(_('name'), max_length=255)
    address = models.TextField(_('address'), blank=True)
    contact_email = models.EmailField(_('contact email'), blank=True)
    contact_phone = models.CharField(
        _('contact phone'), max_length=15, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "fintech\".\"employer"
        verbose_name = _('Employer')
        verbose_name_plural = _('Employers')


class Employee(TimeStampedMixin, UUIDMixin):
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name='employees')
    full_name = models.CharField(_('full name'), max_length=255)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=15, blank=True)
    salary = models.DecimalField(
        _('salary'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    bank_account = models.CharField(_('bank account'), max_length=20)
    bank_name = models.CharField(_('bank name'), max_length=100)
    city = models.CharField(_('city'), max_length=100)

    password = models.CharField(_('password'), max_length=128)

    @property
    def available_amount(self):
        return self.salary * Decimal('0.70')

    def update_available_amount(self, amount_to_subtract):
        if self.available_amount >= amount_to_subtract:
            self.salary = self.salary - amount_to_subtract
            self.save()
        else:
            raise ValueError("Requested amount exceeds available amount")

    def get_all_transactions(self):
        return Transaction.objects.filter(request__employee=self)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "fintech\".\"employee"
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')


class SalaryAdvanceRequest(TimeStampedMixin, UUIDMixin):
    PENDING = 'pendiente'
    APPROVED = 'aprobado'
    REJECTED = 'rechazado'

    STATUS_CHOICES = [
        (PENDING, _('Pendiente')),
        (APPROVED, _('Aprobado')),
        (REJECTED, _('Rechazado')),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='advance_requests')
    amount_requested = models.DecimalField(
        _('amount requested'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(
        _('status'), max_length=20, choices=STATUS_CHOICES, default=PENDING, auto_created=True)
    request_date = models.DateTimeField(_('request date'), default=timezone.now)
    review_date = models.DateTimeField(_('review date'), null=True, blank=True)

    def __str__(self):
        return f"Request {self.id} by {self.employee.full_name}"

    def save(self, *args, **kwargs):
        if self.status == self.APPROVED and not self.review_date:
            self.review_date = timezone.now()
            if hasattr(self, 'employee'):
                self.employee.update_available_amount(self.amount_requested)
        
        super().save(*args, **kwargs)

    class Meta:
        db_table = "fintech\".\"salary_advance_request"
        verbose_name = _('Salary Advance Request')
        verbose_name_plural = _('Salary Advance Requests')


class Transaction(UUIDMixin):
    request = models.ForeignKey(
        SalaryAdvanceRequest, on_delete=models.CASCADE, related_name='transactions')
    transaction_date = models.DateTimeField(
        _('transaction date'), auto_now_add=True)
    amount = models.DecimalField(
        _('amount'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Transaction for {self.request}"

    class Meta:
        db_table = "fintech\".\"transaction"
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
