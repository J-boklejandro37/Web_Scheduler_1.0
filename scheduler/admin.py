from django.contrib import admin
from .models import Tasks, DailyCheckbox

# Register your models here.
admin.site.register(Tasks)
admin.site.register(DailyCheckbox)
