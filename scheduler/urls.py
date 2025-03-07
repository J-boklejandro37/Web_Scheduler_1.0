from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view),
    
    path('home/', views.home_view),
    path('credits/', views.credits_view),
    path('daily/', views.daily_view),
    path('daily/<str:id>/checked/', views.checked, name='checked_url'),
    path('daily/daily_reset/', views.daily_reset),

    path('calendar/', views.calendar_view),
    path('calendar/open_dialog/', views.open_dialog),

    path('settings/', views.settings_view),
    path('settings/change_birthday/', views.change_birthday),
    path('settings/add_task/', views.add_task),
    path('settings/delete_task/<str:id>/', views.delete_task),
    path('settings/add_calendar/', views.add_calendar),
    path('settings/delete_calendar/', views.delete_calendar),
]