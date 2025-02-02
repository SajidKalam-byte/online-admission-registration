from django.contrib import admin
from .models import Counsellor, AdmissionEnquiry

class CounsellorAdmin(admin.ModelAdmin):
    list_display = ['name', 'assigned_students']  # Removed 'email' as it does not exist

class AdmissionEnquiryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone_number', 'assigned_counsellor__name']
    list_filter = ['course_preferred_1', 'reference_source']

admin.site.register(Counsellor, CounsellorAdmin)
admin.site.register(AdmissionEnquiry, AdmissionEnquiryAdmin)
