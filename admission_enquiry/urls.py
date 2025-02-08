from django.urls import path
from . import views

urlpatterns = [
    path('', views.enquiry_form, name='enquiry_form'),  # Landing page
    path('admission_form/', views.admission_form, name='admission_form'),
    path('payment/', views.payment, name='payment'),  # Payment URL
    path('final_step/', views.final_step, name='final_step'), # Final step
    path('download_letter/', views.download_allotment_letter, name='download_letter'),  # Download Allotment Letter
    path('download_invoice/<int:admission_form_id>/', views.download_invoice, name='download_invoice'),
]
