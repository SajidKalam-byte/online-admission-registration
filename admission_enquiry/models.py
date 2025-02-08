from django.db import models
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    if not value.name.endswith(('.pdf', '.docx', '.jpg', '.png')):
        raise ValidationError("Only .pdf, .docx, .jpg, and .png files are allowed.")

class Counsellor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, unique=True, null=True)
    assigned_students = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class AdmissionEnquiry(models.Model):
    name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    course_preferred_1 = models.CharField(max_length=50)
    course_preferred_2 = models.CharField(max_length=50, blank=True, null=True)
    course_preferred_3 = models.CharField(max_length=50, blank=True, null=True)
    reference_source = models.CharField(max_length=50)
    assigned_counsellor = models.ForeignKey(Counsellor, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AdmissionForm(models.Model):
    name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    last_qualification = models.CharField(max_length=100)
    aadhar_number = models.CharField(max_length=12)
    documents = models.FileField(upload_to='supporting_documents/', validators=[validate_file_extension])
    
    def __str__(self):
        return self.name

PAYMENT_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('debit_card', 'Debit Card'),
    ('upi', 'UPI'),
    ('net_banking', 'Net Banking'),
]

class Payment(models.Model):
    admission_form = models.OneToOneField(AdmissionForm, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    payee_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Payment for {self.admission_form.name}"