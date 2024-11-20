from django.http import JsonResponse
from .models import *
from .firebase import auth
import json
from django.views.decorators.http import require_http_methods

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