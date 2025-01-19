import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
from django.core.exceptions import ValidationError

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
    BANCO_UNION = 'Banco Unión S.A.'
    BANCO_MERCANTIL = 'Banco Mercantil Santa Cruz S.A.'
    BANCO_NACIONAL = 'Banco Nacional de Bolivia S.A. (BNB)'
    BANCO_BISA = 'Banco BISA S.A.'
    BANCO_CREDITO = 'Banco de Crédito de Bolivia S.A. (BCP)'
    BANCO_GANADERO = 'Banco Ganadero S.A.'
    BANCO_ECONOMICO = 'Banco Económico S.A.'
    BANCO_SOL = 'BancoSol S.A.'
    BANCO_FIE = 'Banco FIE S.A.'

    BANK_CHOICES = [
        (BANCO_UNION, _('Banco Unión S.A.')),
        (BANCO_MERCANTIL, _('Banco Mercantil Santa Cruz S.A.')),
        (BANCO_NACIONAL, _('Banco Nacional de Bolivia S.A. (BNB)')),
        (BANCO_BISA, _('Banco BISA S.A.')),
        (BANCO_CREDITO, _('Banco de Crédito de Bolivia S.A. (BCP)')),
        (BANCO_GANADERO, _('Banco Ganadero S.A.')),
        (BANCO_ECONOMICO, _('Banco Económico S.A.')),
        (BANCO_SOL, _('BancoSol S.A.')),
        (BANCO_FIE, _('Banco FIE S.A.')),
    ]

    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name='employees')
    full_name = models.CharField(_('full name'), max_length=255)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=15, blank=True)
    salary = models.DecimalField(
        _('salary'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    bank_account = models.CharField(_('bank account'), max_length=20, default="1234567")
    bank_name = models.CharField(
        _('bank name'), 
        max_length=100,
        choices=BANK_CHOICES,
        default=BANCO_UNION
    )    
    
    city = models.CharField(_('city'), max_length=100, default="Santa Cruz de la Sierra")
    password = models.CharField(_('password'), max_length=128)

    def get_current_month_advances(self):
        current_date = timezone.now()
        return SalaryAdvanceRequest.objects.filter(
            employee=self,
            status=SalaryAdvanceRequest.APPROVED,
            review_date__year=current_date.year,
            review_date__month=current_date.month
        ).aggregate(total=Sum('amount_requested'))['total'] or 0

    @property
    def available_amount(self):
        return (self.salary * Decimal('0.70')) - self.get_current_month_advances()

    def update_available_amount(self, amount_to_subtract):
        if self.available_amount >= amount_to_subtract:
            return True
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

    def clean(self):
        if self.amount_requested and self.employee:
            if self.amount_requested > self.employee.available_amount:
                raise ValidationError({
                    'amount_requested': _(
                        'Amount requested (%(requested)s) exceeds available amount (%(available)s)'
                    ) % {
                        'requested': self.amount_requested,
                        'available': self.employee.available_amount,
                    }
                })

    def save(self, *args, **kwargs):
        if self.status == self.APPROVED and not self.review_date:
            self.review_date = timezone.now()
            if hasattr(self, 'employee'):
                self.employee.update_available_amount(self.amount_requested)
        elif self.status == self.REJECTED:
            self.review_date = timezone.now()
        
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
