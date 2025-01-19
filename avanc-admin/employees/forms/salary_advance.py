from django import forms
from django.utils.translation import gettext_lazy as _
from employees.models import SalaryAdvanceRequest

class SalaryAdvanceRequestForm(forms.ModelForm):
    class Meta:
        model = SalaryAdvanceRequest
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:
            old_status = self.instance.status
            new_status = cleaned_data.get('status')
            if old_status in [SalaryAdvanceRequest.APPROVED, SalaryAdvanceRequest.REJECTED] and old_status != new_status:
                raise forms.ValidationError(_('Cannot modify a request that has been approved or rejected'))
        return cleaned_data