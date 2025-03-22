from django.contrib import admin
from django.contrib.auth import get_user_model  # Correct way to get AUTH_USER_MODEL

User = get_user_model()  # Get the actual User model

@admin.register(User)  # This is the preferred way
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')

# OR Alternative way (if you don't want a custom admin class)
# admin.site.register(User)
