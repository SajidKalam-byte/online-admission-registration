from django.urls import path
from . import views

urlpatterns = [
    path('', views.enquiry_form, name='enquiry_form'),  # Landing page
    path('admission_form/', views.admission_form, name='admission_form'),
    path('payment/', views.payment, name='payment'),  # Payment URL
    path('final_step/', views.final_step, name='final_step'),  # Final step
]
