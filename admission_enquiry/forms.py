
from django import forms
from .models import AdmissionEnquiry, AdmissionForm, Payment

class AdmissionEnquiryForm(forms.ModelForm):
    class Meta:
        model = AdmissionEnquiry
        fields = [
            'name', 'parent_name', 'phone_number',
            'course_preferred_1', 'course_preferred_2', 
            'course_preferred_3', 'reference_source'
        ]
        
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone


class AdmissionFormForm(forms.ModelForm):
    class Meta:
        model = AdmissionForm
        fields = [
            'name', 'parent_name', 'phone_number', 'last_qualification', 'aadhar_number', 'documents'
        ]

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'amount', 'payment_mode', 'transaction_id', 'date', 'payee_name'
        ]
