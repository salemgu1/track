from django.contrib import admin
from .models import Doctor,Nurse,Patient,Food,Feedback

# Register your models here.

admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Patient)
admin.site.register(Food)
admin.site.register(Feedback)
