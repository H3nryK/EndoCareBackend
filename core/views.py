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
