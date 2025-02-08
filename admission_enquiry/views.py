from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .forms import AdmissionEnquiryForm, AdmissionFormForm, PaymentForm
from django.contrib import messages
from .models import Counsellor, AdmissionEnquiry, AdmissionForm, Payment
from django.urls import reverse


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
        if form.is_valid():
            try:
                enquiry = form.save(commit=False)
                counsellor = assign_counsellor()
                if counsellor:
                    enquiry.assigned_counsellor = counsellor
                enquiry.save()
                return render(request, 'admission_enquiry/assigned_counsellor.html', {'counsellor': counsellor})
            except Exception as e:
                print(f"Error saving enquiry: {e}")
                messages.error(request, "Error saving your enquiry. Please try again.")
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        form = AdmissionEnquiryForm()
    return render(request, 'admission_enquiry/enquiry_form.html', {'form': form})

def admission_form(request):
    if request.method == 'POST':
        form = AdmissionFormForm(request.POST, request.FILES)
        if form.is_valid():
            admission_form = form.save()
            return redirect(f"/payment/?admission_form_id={admission_form.id}")
        else:
            print("Form errors:", form.errors)  # Debugging line
    else:
        form = AdmissionFormForm()
    return render(request, 'admission_enquiry/admission_form.html', {'form': form})


def payment(request):
    admission_form_id = request.GET.get('admission_form_id')
    if not admission_form_id:
        return HttpResponseBadRequest("Missing 'admission_form_id' parameter.")

    admission_form = get_object_or_404(AdmissionForm, id=admission_form_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.admission_form = admission_form
            payment.save()
            print(f"✅ Payment Successful: {payment.transaction_id}")  # Debugging
            return redirect(reverse('final_step') + f'?admission_form_id={admission_form.id}')
        else:
            print("❌ Payment Form Errors:", form.errors)  # Debugging
    else:
        form = PaymentForm()

    return render(request, 'admission_enquiry/payment.html', {'form': form, 'admission_form': admission_form})


def final_step(request):
    admission_form_id = request.GET.get('admission_form_id')
    if not admission_form_id:
        return HttpResponseBadRequest("Missing 'admission_form_id' parameter.")

    admission_form = get_object_or_404(AdmissionForm, id=admission_form_id)
    payment = get_object_or_404(Payment, admission_form=admission_form)

    return render(request, 'admission_enquiry/final_step.html', {
        'admission_form': admission_form,
        'payment': payment
    })


