
def settings(request):

    if hasattr(request, "user"):
        user_settings = request.user_settings
    else:
        from .models import UserSettings
        user_settings = UserSettings()
        
    return {
        "user_settings": user_settings,
    }