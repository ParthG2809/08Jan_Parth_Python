from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Doctor, Appointment

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'appointments/doctor_list.html', {'doctors': doctors})

def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        patient_email = request.POST.get('patient_email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient_name=patient_name,
            patient_email=patient_email,
            date=date,
            time=time,
            status='Pending'
        )
        return redirect('appointments:payment', appointment_id=appointment.id)
        
    return render(request, 'appointments/book_appointment.html', {'doctor': doctor})

def payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {
        'appointment': appointment,
        'client_id': settings.PAYPAL_CLIENT_ID
    }
    return render(request, 'appointments/payment.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('orderID')
            appointment_id = data.get('appointmentID')
            
            appointment = get_object_or_404(Appointment, id=appointment_id)
            appointment.paypal_order_id = order_id
            appointment.status = 'Paid'
            appointment.save()
            return JsonResponse({'status': 'Success', 'message': 'Payment completed successfully'})
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)})
            
    # For GET request (after JS redirects)
    return render(request, 'appointments/success.html')

def payment_cancel(request):
    return render(request, 'appointments/cancel.html')

