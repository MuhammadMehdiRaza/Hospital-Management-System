from django.shortcuts import render,redirect
from hms.models import Appointment,Patient  # Import the Appointment model
from django.contrib.auth.decorators import login_required # Import login_required



@login_required
def doctor_index(request):
    # Optional: redirect to profile or schedule
   return redirect('login')


@login_required 
def doctor_daily_schedule_view(request):
    """View to display a doctor's daily schedule (initially showing all appointments)."""
    appointments = Appointment.objects.all()  # Fetch all appointments for now
    context = {'appointments': appointments}
    return render(request, 'doctor_app/doctor_daily_schedule.html', context)

   

@login_required
def doctor_profile_view(request):
    # request.user is the logged-in User; .doctor is the linked Doctor profile
    doctor = request.user.doctor
    return render(request, 'doctor_app/doctor_profile.html', {'doctor': doctor})

@login_required
def doctor_patient_list(request):
    patients = Patient.objects.filter(appointments__doctor=request.user.doctor).distinct()
    return render(request, 'doctor_app/doctor_patient_list.html', {'patients': patients})