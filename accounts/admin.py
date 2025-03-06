from django.contrib import admin
from .models import Userbase, Tasks, DailyCheckbox

# Register your models here.
admin.site.register(Userbase)
admin.site.register(Tasks)
admin.site.register(DailyCheckbox)