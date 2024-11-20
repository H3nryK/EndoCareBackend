from django.http import JsonResponse
from .models import UserProfile
from .firebase import auth

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