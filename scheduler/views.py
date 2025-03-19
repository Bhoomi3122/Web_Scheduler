from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Schedule, Task
from django.contrib import messages
from django.db import IntegrityError
from .forms import TaskForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime 
from django.db.models import Case, When, Value, IntegerField
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.user.is_authenticated:
        active_schedules = Schedule.objects.filter(user=request.user, is_completed=False)
        completed_schedules = Schedule.objects.filter(user=request.user, is_completed=True)
        return render(request, "scheduler/index.html", {
            "active_schedules": active_schedules,
            "completed_schedules": completed_schedules
        })
    else:
        return redirect('login')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "scheduler/login.html")
    else:
        return render(request, "scheduler/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "scheduler/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "scheduler/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "scheduler/register.html")
    
def add_schedule(request):
    if request.method == 'POST' and 'create_schedule' in request.POST:
        schedule_title = request.POST.get('schedule_title')
        new_schedule = Schedule.objects.create(
            user=request.user, 
            title=schedule_title,
            is_completed=False
        )

        task_names = request.POST.getlist('task_name')
        descriptions = request.POST.getlist('description')
        start_times = request.POST.getlist('start_time')
        end_times = request.POST.getlist('end_time')

        for i in range(len(task_names)):
            Task.objects.create(
                schedule=new_schedule,
                name=task_names[i],
                description=descriptions[i],
                start_time=start_times[i],
                end_time=end_times[i]
            )

        return redirect('view_schedule')

    return render(request, 'scheduler/add.html')

@login_required
def view_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id, user=request.user)
    
    tasks = list(schedule.tasks.all())

    def convert_time(task):
        return datetime.strptime(task.start_time, "%I:%M %p")

    tasks.sort(key=lambda task: (1 if task.status == "Pending" else 2, convert_time(task)))

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.status == "Completed")
    completion_percentage = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
    progress_bar_class = 'bg-success' if completion_percentage > 0 else 'bg-danger'

    return render(request, "scheduler/view.html", {
        "schedule": schedule,
        "tasks": tasks,
        "completion_percentage": completion_percentage,
        "progress_bar_class": progress_bar_class
    })

def add_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            schedule_id = data.get('schedule_id')
            name = data.get('name') 
            description = data.get('description', '')
            start_time = data.get('start_time')
            end_time = data.get('end_time')

            if not schedule_id or not name or not start_time or not end_time:
                return JsonResponse({'success': False, 'error': 'Missing required fields'})

            schedule = Schedule.objects.get(id=schedule_id)

            task = Task.objects.create(
                schedule=schedule,
                name=name, 
                description=description,
                start_time=start_time,
                end_time=end_time
            )

            return JsonResponse({'success': True, 'message': 'Task added successfully!'})

        except Schedule.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Schedule not found'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def create_schedule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            schedule_title = data.get('schedule_title')
            tasks = data.get('tasks')

            schedule = Schedule.objects.create(
                user=request.user,
                title=schedule_title
            )

            for task in tasks:
                Task.objects.create(
                    schedule=schedule,
                    name=task["name"],
                    description=task["description"],
                    start_time=task["start_time"],
                    end_time=task["end_time"]
                )

            return JsonResponse({'success': True, 'schedule_id': schedule.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'DELETE':
        task = get_object_or_404(Task, id=task_id)
        schedule = task.schedule
        task.delete()

        tasks = Task.objects.filter(schedule=schedule)
        total_tasks = tasks.count()

        if total_tasks > 0:
            completed_tasks = tasks.filter(status='Completed').count()
            completion_percentage = int((completed_tasks / total_tasks) * 100)
            
            if completion_percentage == 100:
                schedule.is_completed = True
                schedule.save()
        else:
            schedule.delete()
            return JsonResponse({'message': 'Task and schedule deleted successfully.', 
                                 'schedule_deleted': True, 'redirect_url': '/'}, status=200)

        return JsonResponse({'message': 'Task deleted successfully.', 'schedule_deleted': False}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
@csrf_exempt
def complete_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.status = 'Completed'
            task.save()

            tasks = Task.objects.filter(schedule=task.schedule)
            completed_tasks = tasks.filter(status='Completed').count()
            total_tasks = tasks.count()
            completion_percentage = int((completed_tasks / total_tasks) * 100)

            schedule_completed = False
            if completion_percentage == 100:
                task.schedule.is_completed = True
                task.schedule.save()
                schedule_completed = True

            return JsonResponse({
                'success': True,
                'completion_percentage': completion_percentage,
                'schedule_completed': schedule_completed
            })
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
  
@csrf_exempt
def edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.name = request.POST.get('name')
        task.description = request.POST.get('description')
        task.start_time = request.POST.get('start_time')
        task.end_time = request.POST.get('end_time')
        task.save()
        return redirect(reverse('view_schedule', args=[task.schedule.id]))

    start_parts = task.start_time.split(" ")  # ["10:30", "PM"]
    start_hour, start_minute = start_parts[0].split(":")  # ["10", "30"]
    start_period = start_parts[1]  # "PM"

    end_parts = task.end_time.split(" ")  # ["02:15", "AM"]
    end_hour, end_minute = end_parts[0].split(":")  # ["02", "15"]
    end_period = end_parts[1]  # "AM"

    return render(request, 'scheduler/edit.html', {
        'task': task,
        'start_hour': start_hour,
        'start_minute': start_minute,
        'start_period': start_period,
        'end_hour': end_hour,
        'end_minute': end_minute,
        'end_period': end_period
    })
