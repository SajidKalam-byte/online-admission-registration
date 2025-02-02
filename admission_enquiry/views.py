from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .forms import AdmissionEnquiryForm, AdmissionFormForm, PaymentForm
from django.contrib import messages
from .models import Counsellor, AdmissionEnquiry, AdmissionForm, Payment

def assign_counsellor():
    try:
        counsellors = Counsellor.objects.order_by('assigned_students')
        if counsellors.exists():
            selected = counsellors.first()
            selected.assigned_students += 1
            selected.save()
            return selected
        return None
    except Exception as e:
        print(f"Error assigning counsellor: {e}")
        return None

def enquiry_form(request):
    if request.method == 'POST':
        form = AdmissionEnquiryForm(request.POST)
        print("Form submitted")
        
        if form.is_valid():
            print("Form is valid")
            try:
                enquiry = form.save(commit=False)
                counsellor = assign_counsellor()
                print(f"Assigned counsellor: {counsellor}")
                
                if counsellor:
                    enquiry.assigned_counsellor = counsellor
                
                enquiry.save()
                print("Enquiry saved successfully")
                
                # Redirect to assigned_counsellor page
                return render(
                    request,
                    'admission_enquiry/assigned_counsellor.html',
                    {'counsellor': counsellor}
                )
            except Exception as e:
                print(f"Error saving enquiry: {e}")
                messages.error(request, "Error saving your enquiry. Please try again.")
    
    form = AdmissionEnquiryForm()
    return render(request, 'admission_enquiry/enquiry_form.html', {'form': form})

def admission_form(request):
    if request.method == 'POST':
        form = AdmissionFormForm(request.POST, request.FILES)
        if form.is_valid():
            admission_form = form.save()
            return redirect(f"/payment/?admission_form_id={admission_form.id}")
    else:
        form = AdmissionFormForm()
    return render(request, 'admission_enquiry/admission_form.html', {'form': form})

def payment(request):
    admission_form_id = request.GET.get('admission_form_id')

    if not admission_form_id:
        return HttpResponseBadRequest("Missing 'admission_form_id' parameter.")

    try:
        admission_form_id = int(admission_form_id)
    except ValueError:
        return HttpResponseBadRequest("Invalid 'admission_form_id' parameter.")

    admission_form = get_object_or_404(AdmissionForm, id=admission_form_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.admission_form = admission_form
            payment.save()
            return redirect('/final_step/')
    else:
        form = PaymentForm()

    return render(request, 'admission_enquiry/payment.html', {'form': form, 'admission_form': admission_form})

def final_step(request):
    return render(request, 'admission_enquiry/final_step.html')
