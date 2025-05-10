from google import genai
from django.shortcuts import render,redirect
from hms.models import Appointment,Patient,LabTestOrder  # Import the Appointment model
from django.contrib.auth.decorators import login_required # Import login_required
from .forms import DoctorProfileForm,LabTestOrderForm

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


def edit_profile(request):
    doctor = request.user.doctor  
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_app:doctor_profile')
    else:
        form = DoctorProfileForm(instance=doctor)
    return render(request, 'doctor_app/edit_profile.html', {'form': form})

def AI_CHATBOT(request):
    """View for interacting with the Gemini AI chatbot."""    
    api_key = 'AIzaSyC1Cc6EhFY0l8sHteIO7IW14aZvoADZPHI'
    chat_history = []  
    
    if api_key:
        client = genai.Client(api_key=api_key) 

        if request.method == 'POST':
            user_message = request.POST.get('user_message', '')
            
            if user_message:
                try:
                    response = client.models.generate_content(
                    model="gemini-2.0-flash", contents=user_message
                    )
                    response_text = response.text
                    
                    chat_history.append({
                        'user': user_message,
                        'bot': response_text
                    })
                    
                    if 'chat_history' not in request.session:
                        request.session['chat_history'] = []
                    
                    request.session['chat_history'].append({
                        'user': user_message,
                        'bot': response_text
                    })
                    request.session.modified = True
                    
                except Exception as e:
                    chat_history.append({
                        'user': user_message,
                        'bot': f"Error communicating with AI service: {str(e)}"
                    })
        else:
            chat_history = request.session.get('chat_history', [])
    
    context = {
        'chat_history': chat_history,
        'api_configured': bool(api_key)
    }
    # print("Chat history:", chat_history)  
    return render(request, 'doctor_app/ai_chatbot.html', context)

@login_required
def order_lab_test(request):
    doctor = request.user.doctor
    if request.method == 'POST':
        form = LabTestOrderForm(request.POST)
        if form.is_valid():
            lab_order = form.save(commit=False)
            lab_order.doctor = doctor
            lab_order.save()
            return redirect('doctor_app:doctor_profile')
    else:
        form = LabTestOrderForm()
    return render(request, 'doctor_app/order_lab_test.html', {'form': form})