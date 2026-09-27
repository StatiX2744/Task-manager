from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django import forms

from .tasks import *
from .teams import *
from .forms import RegisterForm, LoginForm, CreateTaskForm, DeleteTaskForm, CreateTeamForm
from .TaskChecker import TaskChecker
from .models import User, Task


def user_login(request):
    '''
    Route to log into an account.
    '''

    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('/tasks')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'login.html',{'form': form})
    

def register(request):
    '''
    Route create a new account.
    '''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def sign_out(request):
    '''
    Route to sign out.
    '''
    logout(request)
    return redirect('/login')


def tasks(request):
    '''
    Route to display all tasks that you should be able
    to see.
    '''
    if request.user.is_authenticated:
        #display tasks
        if request.method == "GET":
            myTasks = [(t,doableTaskById(request.user,t.id), request.user == t.createdBy) for t in get_visible_tasks(request.user)]
            return render(request, 'tasks.html',{'myTasks':myTasks})
        if request.method == "POST":
            pass
    else:
        return redirect('/login')

def create_tasks(request):
    '''
    Route to create a new task.
    '''
    if request.user.is_authenticated:
        create_message = ""
        #create a task
        if request.method == 'POST':
            form = CreateTaskForm(request.POST)
            taskChecker = TaskChecker()
            taskValidityChecker(form, request.user, taskChecker)
            if taskChecker.validity == 0:
                createTask(form,request.user, taskChecker)
                create_message = "Tâche créée avec succès"
            elif taskChecker.validity == 1:
                create_message = "Un des utilisateurs indiqués n'existe pas."
            elif taskChecker.validity == 2:
                create_message = "Une des équipes indiquées n'existe pas."
                
        else:
            form = CreateTaskForm()

        return render(request, 'create_tasks.html', {'form': form,'create_message': create_message,'typeTask': 0})
    return redirect('/login')

def create_subtasks(request, parent_id):
    '''
    Route to create a subtask from a task.
    '''
    if request.user.is_authenticated:
        create_message = ""
        try:
            Task.objects.get(id=parent_id)
        except Task.DoesNotExist:
            return redirect('/tasks')
            
        if not(doableTaskById(request.user,parent_id)):
            return redirect('/tasks')
        
        #create a task
        if request.method == 'POST':
            form = CreateTaskForm(request.POST)
            taskChecker = TaskChecker()
            subTaskValidityChecker(form, request.user, taskChecker, parent_id)
            if taskChecker.validity == 0:
                createTask(form,request.user, taskChecker)
                create_message = "Tâche créée avec succès"
            elif taskChecker.validity == 1:
                create_message = "Un des utilisateurs indiqués n'existe pas."
            elif taskChecker.validity == 2:
                create_message = "Une des équipes indiquées n'existe pas."
                
        else:

            form = CreateTaskForm()

        return render(request, 'create_tasks.html', {'form': form,'create_message': create_message,'typeTask': 1})
    return redirect('/login')

def do_tasks(request, task_id):
    '''
    Route to mark a task as "done".
    '''
    if request.user.is_authenticated:
        try:
            Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return redirect('/tasks')
        
        if(doableTaskById(request.user,task_id)):
            doTask(task_id)
        return redirect('/tasks')
    return redirect('/login')

def undo_tasks(request, task_id):
    '''
    Route to mark a task as "not done".
    '''
    if request.user.is_authenticated:
        try:
            Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return redirect('/tasks')
        
        if(doableTaskById(request.user,task_id)):
            undoTask(task_id)
        return redirect('/tasks')
    return redirect('/login')

def update_tasks(request, task_id):
    '''
    Route to edit a task.
    '''
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return redirect('/tasks')
        update_message = ""

        if request.method == 'POST':    
            form = CreateTaskForm(request.POST)
            taskChecker = TaskChecker()
            taskValidityChecker(form, request.user, taskChecker)

            if taskChecker.validity == 0:
                updateTask(form,task, taskChecker)
                update_message = "Tâche modifiée avec succès"
            elif taskChecker.validity == 1:
                update_message = "Un des utilisateurs indiqués n'existe pas."
            elif taskChecker.validity == 2:
                update_message = "Une des équipes indiquées n'existe pas."



        else:
            form = CreateTaskForm()
            
        return render(request, 'create_tasks.html', {'form': form,'create_message': update_message,'typeTask': 2})
    return redirect('/login')

def delete_tasks(request):
    '''
    Route to delete a task.
    '''
    if request.user.is_authenticated:
        delete_message = ""
        #delete a task
        if request.method == 'POST':
            form = DeleteTaskForm(request.POST)
            if deletableTask(form,request.user) == True:
                deleteTask(form)
                delete_message = "Tâche supprimée avec succès !"
            else:
                delete_message = "La tâche associée à ce numéro n'existe pas ou vous ne pouvez pas la supprimer !"
        else:
            form = DeleteTaskForm()

        return render(request, 'delete_tasks.html', {'form': form,'delete_message': delete_message})
    return redirect('/login')

def task_inspect(request, task_id):
    '''
    Route to get more information about a task.
    '''
    if request.user.is_authenticated:
        if request.method == 'GET':
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return redirect('/tasks')
            
            assigned_users = getUsersAssignedToTask(task)
            assigned_teams = getTeamsAssignedToTask(task)

            return render(request, "task_inspect.html", 
                {"task" : (task,doableTaskById(request.user,task.id)), "Assigned_users": assigned_users, "Assigned_teams" : assigned_teams})
    return redirect('/login')

def index(request):
    '''
    Route of the index.
    '''
    return render(request,'index.html')

def users(request, user_id):
    '''
    Route to display information about a certain user.
    '''
    if request.user.is_authenticated:
        if request.method == 'GET':
            profile_user = User.objects.get(id=user_id)
            return render(request, "users.html", 
                {"user" : profile_user,
                "userTasks": [t for t in get_visible_tasks(request.user) if t.createdBy == profile_user]})
    return redirect('/login')


def teams(request):
    '''
    Route to display all teams.
    '''
    if request.method == "GET":
        Teams = [(t,joinableTeam(request.user,t.name),t.createdBy == request.user) for t in getAllTeams()]
        return render(request, 'teams.html',{'Teams':Teams})
    if request.method == "POST":
        pass
    return redirect('/login')

def create_teams(request):
    '''
    Route to create a new team.
    '''
    if request.user.is_authenticated:
        create_message = ""
        #create a task
        if request.method == 'POST':
            form = CreateTeamForm(request.POST)
            name = form['name'].value()
            if teamValidityChecker(name) == False:
                create_message = "Une équipe avec ce nom existe déjà !"
            else:
                createTeam(request.user,name)
                create_message = "Équipe créée avec succès"

        else:
            form = CreateTeamForm()

        return render(request, 'create_teams.html', {'form': form,'create_message': create_message})
    return redirect('/login')


def join_teams(request, team_name):
    '''
    Route to join a team.
    '''
    if request.user.is_authenticated:
        if(joinableTeam(request.user,team_name)):
            joinTeam(request.user,team_name)
        return redirect('/teams')
    return redirect('/login')

def leave_teams(request, team_name):
    '''
    Route to leave a team.
    '''
    if request.user.is_authenticated:
        if(leavableTeam(request.user,team_name)):
            leaveTeam(request.user,team_name)
        return redirect('/teams')
    return redirect('/login')

def delete_teams(request, team_name):
    '''
    Route to delete a team.
    '''
    if request.user.is_authenticated:
        team = getTeamFromName(team_name)
        if(team.createdBy == request.user):
            deleteTeam(team)
        return redirect('/teams')
    return redirect('/login')

def team_inspect(request, team_name):
    '''
    Route to get more informations on a team.
    '''
    if request.user.is_authenticated:
        if request.method == 'GET':
            team = getTeamFromName(team_name)
            members = getTeamMembers(team)
            visible_tasks = [(t,doableTaskById(request.user,t.id)) for t in getTeamTasks(team) if visibleTask(request.user,t)]
            return render(request, "team_inspect.html", 
                {"Team" : team, "Members": members, "Tasks" : visible_tasks})
    return redirect('/login')
