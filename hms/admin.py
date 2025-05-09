from django.contrib import admin
from .models import Patient, Doctor, Appointment, Billing
from auditlog.registry import auditlog
import csv
from django.http import HttpResponse

# Register models with auditlog (must come before admin registration)
auditlog.register(Patient)
auditlog.register(Appointment)

# Standard admin registrations
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Billing)

# Custom admin for Appointments
admin.site.register(Appointment)
