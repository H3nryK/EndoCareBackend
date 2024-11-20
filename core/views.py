from django.http import JsonResponse
from .models import *
from .firebase import auth
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect, csrf_exempt

def sync_user_data(request, uid):
    try:
        # Fetch user details from Firebase
        user_record = auth.get_user(uid)
        user_data = {
            "uid": user_record.uid,
            "name": user_record.display_name,
            "email": user_record.email,
            "profile_picture": user_record.photo_url,
        }

        # Update or create the user profile
        user, created = UserProfile.objects.update_or_create(
            uid=user_data["uid"],
            defaults={
                "name": user_data["name"],
                "email": user_data["email"],
                "profile_picture": user_data["profile_picture"],
            },
        )

        return JsonResponse({"status": "success", "user": user_data}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
def get_user_profile(request, uid):
    if request.method == "GET":
        try:
            user_profile = UserProfile.objects.get(uid=uid)
            data = {
                "uid": user_profile.uid,
                "name": user_profile.name,
                "email": user_profile.email,
                "profile_picture": user_profile.profile_picture,
                "next_period": user_profile.next_period,
                "cycle_length": user_profile.cycle_length,
                "last_period": user_profile.last_period,
                "tracked_cycles": user_profile.tracked_cycles,
                "logged_symptoms": user_profile.logged_symptoms,
            }
            return JsonResponse(data, status=200)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User profile not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)

def edit_user_profile(request, uid):
    if request.method == "POST":
        try:
            user_profile = UserProfile.objects.get(uid=uid)
            data = json.loads(request.body)

            # Use .get() with default values to prevent KeyError
            user_profile.name = data.get("name", user_profile.name)
            user_profile.last_period = data.get("last_period", user_profile.last_period)
            user_profile.cycle_length = data.get("cycle_length", user_profile.cycle_length)
            user_profile.next_period = data.get("next_period", user_profile.next_period)
            
            user_profile.save()

            return JsonResponse({"status": "success", "message": "Profile updated"}, status=200)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User profile not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def add_medication(request, uid):
    try:
        # Find the user profile
        user_profile = UserProfile.objects.get(uid=uid)
        
        # Parse request data
        data = json.loads(request.body)
        
        # Create medication
        medication = Medication.objects.create(
            user_profile=user_profile,
            name=data.get('name', ''),
            dosage=data.get('dosage', ''),
            frequency=data.get('frequency', ''),
            notify=data.get('notify', False)
        )
        
        return JsonResponse({
            'status': 'success', 
            'medication': {
                'id': medication.id,
                'name': medication.name,
                'dosage': medication.dosage,
                'frequency': medication.frequency,
                'notify': medication.notify
            }
        }, status=201)
    
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def get_medications(request, uid):
    try:
        # Find the user profile
        user_profile = UserProfile.objects.get(uid=uid)
        
        # Get all medications for this user
        medications = Medication.objects.filter(user_profile=user_profile)
        
        # Convert to list of dictionaries
        medication_list = [{
            'id': med.id,
            'name': med.name,
            'dosage': med.dosage,
            'frequency': med.frequency,
            'notify': med.notify
        } for med in medications]
        
        return JsonResponse({
            'status': 'success', 
            'medications': medication_list
        }, status=200)
    
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def add_appointment(request, uid):
    try:
        # Find the user profile
        user_profile = UserProfile.objects.get(uid=uid)
        
        # Parse request data
        data = json.loads(request.body)
        
        # Create appointment
        appointment = Appointment.objects.create(
            user_profile=user_profile,
            doctor=data.get('doctor', ''),
            location=data.get('location', ''),
            date=data.get('date', None),
            notify=data.get('notify', False)
        )
        
        return JsonResponse({
            'status': 'success', 
            'appointment': {
                'id': appointment.id,
                'doctor': appointment.doctor,
                'location': appointment.location,
                'date': str(appointment.date),
                'notify': appointment.notify
            }
        }, status=201)
    
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def get_appointments(request, uid):
    try:
        # Find the user profile
        user_profile = UserProfile.objects.get(uid=uid)
        
        # Get all appointments for this user
        appointments = Appointment.objects.filter(user_profile=user_profile)
        
        # Convert to list of dictionaries
        appointment_list = [{
            'id': appt.id,
            'doctor': appt.doctor,
            'location': appt.location,
            'date': str(appt.date),
            'notify': appt.notify
        } for appt in appointments]
        
        return JsonResponse({
            'status': 'success', 
            'appointments': appointment_list
        }, status=200)
    
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def set_periods(request, uid):

    try:
        user_profile = UserProfile.objects.get(uid=uid)

        # Parse request data
        data = json.loads(request.body)

        # Create periods
        periods = Periods.objects.create(
            user_profile=user_profile,
            start_date=data.get('start_date', None),
            cycle_length=data.get('cycle_length', None),
            period_duration=data.get('period_duration', None),
        )

        return JsonResponse({
            'status': 'success',
            'periods': {
                'id': periods.id,
                'start_date': str(periods.start_date),
                'cycle_length': periods.cycle_length,
                'period_duration': periods.period_duration,
            }
        }, status = 201)
    
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_periods(request, uid):
    try:
        # Find the user profile
        user_profile = UserProfile.objects.get(uid=uid)

        # Get all periods for this user
        periods = Periods.objects.filter(user_profile=user_profile)

        # Convert to list of dictionaries
        periods_list = [{
            'id': period.id,
            'start_date': str(period.start_date),
            'cycle_length': period.cycle_length,
            'period_duration': period.period_duration,
        } for period in periods]

        return JsonResponse({
            'status': 'success',
            'periods': periods_list
        }, status=200)

    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def save_endobot_message(request):
    try:
        # Parse the incoming JSON data
        data = json.loads(request.body)
        
        # Extract necessary information
        user_profile_id = data.get('user_profile_id')
        message = data.get('message')
        is_user = data.get('is_user', False)

        # Validate required fields
        if not user_profile_id or not message:
            return JsonResponse({
                'status': 'error', 
                'message': 'Missing required fields'
            }, status=400)

        # Retrieve the user profile
        try:
            user_profile = UserProfile.objects.get(id=user_profile_id)
        except UserProfile.DoesNotExist:
            return JsonResponse({
                'status': 'error', 
                'message': 'User profile not found'
            }, status=404)

        # Create the EndoBot message
        endobot_message = EndoBot.objects.create(
            user_profile=user_profile,
            message=message,
            bot="EndoBot" if not is_user else "User"
        )

        return JsonResponse({
            'status': 'success', 
            'message_id': endobot_message.id
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error', 
            'message': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def save_quizes(request, uid):
    