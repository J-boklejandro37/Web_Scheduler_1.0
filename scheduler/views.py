from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
import datetime
import calendar
from Web_Scheduler.custom import login_required_custom
from accounts.models import Userbase
from .models import Tasks, DailyCheckbox

def test_view(request):
    print(request.session["user_id"])
    birthday = Userbase.objects.get(id=request.session["user_id"]).birthday
    print(birthday.year)
    context = {}
    return render(request, "test.html", context)

@login_required_custom
def home_view(request):
    birthday = Userbase.objects.get(id=request.session["user_id"]).birthday
    context = {
        "birthday": birthday,
        "current_year": datetime.datetime.now().year,
        "age": datetime.datetime.now().year - birthday.year,
        "avg_death_year": birthday.year + 80,
        "hundred_year": birthday.year + 100,
        "remain_year": birthday.year + 80 - datetime.datetime.now().year,
    }
    return render(request, "home.html", context)

@login_required_custom
def credits_view(request):
    context = {}
    return render(request, "credits.html", context)

@login_required_custom
def daily_view(request):
    date_str = datetime.date.today()
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    try:
        daily_checkbox = DailyCheckbox.objects.filter(user_id=request.session["user_id"])
    except:
        daily_checkbox = None

    morning_task = None
    afternoon_task = None
    evening_task = None
    try:
        tasks = Tasks.objects.filter(user_id=request.session["user_id"], date=date_str)
        for task in tasks:
            match task.task_time:
                case "m":
                    morning_task = task
                case "a":
                    afternoon_task = task
                case "e":
                    evening_task = task
    except:
        pass

    context = {
        "year": year,
        "month": month,
        "day": day,
        "daily_checkbox": daily_checkbox,
        "morning_task": morning_task,
        "afternoon_task": afternoon_task,
        "evening_task": evening_task,
    }
    return render(request, "daily_task.html", context)

def checked(request, id=None):
    task = DailyCheckbox.objects.get(id=id)
    if not task.checked:
        task.checked = True
    else:
        task.checked = False
    task.save()
    context = {
        "task": model_to_dict(task),
    }
    return JsonResponse(context, status=200)

def daily_reset(request):
    try:
        daily_checkbox = DailyCheckbox.objects.filter(user_id=request.session["user_id"])
    except:
        daily_checkbox = None

    checkbox_list = []
    for item in daily_checkbox:
        item.checked = False
        item.save()
        checkbox_list.append(model_to_dict(item))
        
    context = {
        "checkbox_list": checkbox_list,
    }
    return JsonResponse(context, status=200)

@login_required_custom
def calendar_view(request):
    year = datetime.date.today().year
    month = datetime.date.today().month

    if request.method == "POST":
        month_str = request.POST.get("set_month")
        set_month = datetime.datetime.strptime(month_str, "%Y-%m")
        year = set_month.year
        month = set_month.month

    month_range = calendar.monthrange(year, month)
    week_start = (month_range[0] + 1) % 7
    month_length = month_range[1]
    cal_range = range(1, month_length + 1)

    #get tasks in calendar
    calendar_list = []
    for day in cal_range:
        day_dict = {}
        day_dict["day"] = day
        try:
            day_dict["morning"] = Tasks.objects.filter(date=datetime.date(year, month, day), task_time="m").first()
        except:
            day_dict["morning"] = None
        try:
            day_dict["afternoon"] = Tasks.objects.filter(date=datetime.date(year, month, day), task_time="a").first()
        except:
            day_dict["afternoon"] = None
        try:
            day_dict["evening"] = Tasks.objects.filter(date=datetime.date(year, month, day), task_time="e").first()
        except:
            day_dict["evening"] = None
        calendar_list.append(day_dict)
        print(day_dict)

    context = {
        "month_value": str(year) + "-" + str(month).zfill(2),
        "cal_range": cal_range,
        "start_offset": range(1, week_start + 1),
        "calendar_list": calendar_list,
    }
    return render(request, "calendar.html", context)

def open_dialog(request):
    date = request.POST.get("date")
    obj_list = Tasks.objects.filter(user_id=request.session["user_id"], date=date)
    morning_task = None
    afternoon_task = None
    evening_task = None
    if obj_list:
        print("here")
        for task in obj_list:
            match task.task_time:
                case "m":
                    morning_task = model_to_dict(task)
                case "a":
                    afternoon_task = model_to_dict(task)
                case "e":
                    evening_task = model_to_dict(task)

    context = {
        "morning_task": morning_task,
        "afternoon_task": afternoon_task,
        "evening_task": evening_task,
    }

    return JsonResponse(context, status=200)

@login_required_custom
def settings_view(request):
    try:
        daily_checkbox = DailyCheckbox.objects.filter(user_id=request.session["user_id"])
    except:
        daily_checkbox = None

    context = {
        "daily_checkbox": daily_checkbox,
    }
    return render(request, "settings.html", context)

def change_birthday(request):
    context = {}
    if request.method == "POST":
        new_date = request.POST.get("date")
        password = request.POST.get("password")
        if not new_date:
            context["response"] = "Date not Entered."
        elif not password:
            context["response"] = "Password not Entered."
        elif not check_password(password, make_password(password)):
            context["response"] = "Password Incorrect."
        else:
            obj = Userbase.objects.get(id=request.session["user_id"])
            obj.birthday = new_date
            obj.save()
            context["response"] = "Birthday Updated."
    
    return JsonResponse(context, status=200)

def add_task(request):
    
    task = request.POST.get("task")
    obj = DailyCheckbox.objects.create(user_id=request.session["user_id"], task=task)
    context = {
        "task": model_to_dict(obj),
    }
    
    return JsonResponse(context, status=200)

def delete_task(request, id=None):
    context = {}
    item = DailyCheckbox.objects.get(id=id)
    item.delete()
    
    return JsonResponse(context, status=200)

def add_calendar(request):
    context = {}    
    date_str = request.POST.get("task_date")    
    title = request.POST.get("task_title")
    time = request.POST.get("task_time")    

    if not date_str:
        context["response"] = "Please select a date."
    elif not title:
        context["response"] = "Please enter a title."
    elif not time:
        context["response"] = "Please select a time."
    else:
        try:
            content = request.POST.get("task_content")
        except:
            content = None
        match time:
            case "Morning":
                time_abbr = "m"
            case "Afternoon":
                time_abbr = "a"
            case "Evening":
                time_abbr = "e"
        Tasks.objects.create(user_id=request.session["user_id"], date=date_str, task_title=title, task_content=content, task_time=time_abbr)
        context["response"] = "Task Created."

    return JsonResponse(context, status=200)

def delete_calendar(request):
    context = {}

    return JsonResponse(context, status=200)
