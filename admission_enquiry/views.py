from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .forms import AdmissionEnquiryForm, AdmissionFormForm, PaymentForm
from django.contrib import messages
from .models import Counsellor, AdmissionEnquiry, AdmissionForm, Payment
from django.urls import reverse
from .models import AdmissionForm
from reportlab.pdfgen import canvas 
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import AdmissionForm

def download_invoice(request, admission_form_id):  # Accept admission_form_id as an argument
    admission_form = get_object_or_404(AdmissionForm, id=admission_form_id)
    payment = get_object_or_404(Payment, admission_form=admission_form)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{admission_form.name}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "XYZ Institute of Technology")
    p.setFont("Helvetica", 12)
    p.drawString(200, height - 70, "123, ABC Road, City, Country - 567890")
    p.drawString(200, height - 90, "Email: info@xyzinstitute.com | Phone: +91-1234567890")

    p.line(50, height - 100, width - 50, height - 100)

    # Invoice Title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(250, height - 130, "Fee Payment Invoice")

    # Invoice Details
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 160, f"Invoice No: INV-{payment.id}")
    p.drawString(50, height - 180, f"Student Name: {admission_form.name}")
    p.drawString(50, height - 200, f"Transaction ID: {payment.transaction_id}")
    p.drawString(50, height - 220, f"Payment Date: {payment.date.strftime('%d-%m-%Y')}")
    p.drawString(50, height - 240, f"Payment Method: {payment.get_payment_mode_display()}")
    p.drawString(50, height - 260, f"Amount Paid: Rs. {payment.amount}")

    # Footer
    p.line(50, 100, width - 50, 100)
    p.drawString(50, 80, "Authorized Signatory")
    p.drawString(50, 60, "XYZ Institute of Technology")

    p.showPage()
    p.save()
    return response


def download_allotment_letter(request):
    admission_form_id = request.GET.get('admission_form_id')
    if not admission_form_id:
        return HttpResponse("Missing 'admission_form_id' parameter.", status=400)

    admission_form = get_object_or_404(AdmissionForm, id=admission_form_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Allotment_Letter_{admission_form.name}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Header (Institute Name and Logo)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(150, height - 50, "XYZ Institute of Technology")
    p.setFont("Helvetica", 12)
    p.drawString(150, height - 70, "123, ABC Road, City, Country - 567890")
    p.drawString(150, height - 90, "Email: info@xyzinstitute.com | Phone: +91-1234567890")

    # Draw Line
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    p.line(50, height - 100, width - 50, height - 100)

    # Title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(220, height - 130, "Admission Allotment Letter")

    # Student Details Table
    data = [
        ["Student Name:", admission_form.name],
        ["Parent's Name:", admission_form.parent_name],
        ["Phone Number:", admission_form.phone_number],
        ["Aadhar Number:", admission_form.aadhar_number],
        ["Last Qualification:", admission_form.last_qualification],
        ["Course Opted:", "Not Available"],  # Replace if available
    ]

    table = Table(data, colWidths=[200, 250])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(p, width, height)
    table.drawOn(p, 50, height - 300)

    # Allotment Message
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 360, "Dear Student,")
    p.drawString(50, height - 380, "Congratulations! You have been allotted a seat at XYZ Institute.")
    p.drawString(50, height - 400, "Please complete further formalities at the institute office.")

    # Footer
    p.line(50, 100, width - 50, 100)
    p.drawString(50, 80, "Authorized Signatory")
    p.drawString(50, 60, "XYZ Institute of Technology")

    p.showPage()
    p.save()
    return response



# def download_invoice(request, admission_form_id):
#     admission_form = get_object_or_404(AdmissionForm, id=admission_form_id)
#     payment = get_object_or_404(Payment, admission_form=admission_form)

#     # Create PDF response
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="Invoice_{admission_form.name}.pdf"'

#     # Generate PDF using reportlab
#     p = canvas.Canvas(response)
#     p.setFont("Helvetica-Bold", 16)
#     p.drawString(200, 800, "Invoice")

#     p.setFont("Helvetica", 12)
#     p.drawString(100, 750, f"Student Name: {admission_form.name}")
#     p.drawString(100, 730, f"Parent's Name: {admission_form.parent_name}")
#     p.drawString(100, 710, f"Phone Number: {admission_form.phone_number}")
#     p.drawString(100, 690, f"Aadhar Number: {admission_form.aadhar_number}")

#     p.drawString(100, 650, f"Amount Paid: Rs. {payment.amount}")
#     p.drawString(100, 630, f"Payment Mode: {payment.get_payment_mode_display()}")
#     p.drawString(100, 610, f"Transaction ID: {payment.transaction_id}")
#     p.drawString(100, 590, f"Payment Date: {payment.date}")

#     p.showPage()
#     p.save()

#     return response
# def download_allotment_letter(request):
#     admission_form_id = request.GET.get('admission_form_id')
#     if not admission_form_id:
#         return HttpResponse("Missing 'admission_form_id' parameter.", status=400)

#     admission_form = get_object_or_404(AdmissionForm, id=admission_form_id)

#     # Create the PDF response
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="Allotment_Letter_{admission_form.name}.pdf"'

#     # Generate PDF using reportlab
#     p = canvas.Canvas(response)
#     p.setFont("Helvetica-Bold", 16)
#     p.drawString(200, 800, "Admission Allotment Letter")

#     p.setFont("Helvetica", 12)
#     p.drawString(100, 750, f"Student Name: {admission_form.name}")
#     p.drawString(100, 730, f"Parent's Name: {admission_form.parent_name}")  # ✅ Fixed
#     p.drawString(100, 710, f"Course Opted: Not Available")  # ⚠️ Add course field if needed

#     p.drawString(100, 670, "Congratulations! You have been allotted a seat in our institution.")
#     p.drawString(100, 650, "Please keep this document for future reference.")

#     p.showPage()
#     p.save()

#     return response


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


