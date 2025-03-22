from django.contrib import admin
from .models import Shift, Nurse, Availability


admin.site.register(Nurse)
admin.site.register(Shift)
admin.site.register(Availability)