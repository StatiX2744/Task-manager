from .models import User, Team, Task, AssignUserToTask, AssignTeamToTask, AssignUserToTeam
from .TaskChecker import TaskChecker

import re

def taskValidityChecker(form, user, taskChecker):
    '''
    Checks if the form info results in a valid task.
    '''
    taskChecker.list_of_allowed_users = [elt for elt in re.split(' |,|;',form['userList'].value()) if elt != '']
    taskChecker.list_of_allowed_teams = [elt for elt in re.split(' |,|;',form['teamList'].value()) if elt != '']

    users = User.objects.all().values_list('username', flat=True)
    teams = Team.objects.all().values_list('name', flat=True)
    tasks = Task.objects.all()

    taskChecker.parentTask = None

    for u in taskChecker.list_of_allowed_users:
        if u not in users:
            taskChecker.validity = 1
            return taskChecker

    for t in taskChecker.list_of_allowed_teams:
        if t not in teams:
            taskChecker.validity = 2
            return taskChecker
    
    taskChecker.validity = 0
    return taskChecker

def subTaskValidityChecker(form, user, taskChecker, parent_id):
    '''
    Checks if the form info results in a valid subtask.
    '''
    taskValidityChecker(form,user,taskChecker)
    if(taskChecker.validity != 0):
        return taskChecker

    try:
        taskChecker.parentTask = Task.objects.get(id=parent_id)
    except Task.DoesNotExist:
        taskChecker.validity = 3
        return taskChecker

    tasks = Task.objects.all()
    if taskChecker.parentTask is not None:
        if taskChecker.parentTask not in tasks:
            taskChecker.validity = 3
            return taskChecker
    return taskChecker


def createTask(form, user, taskChecker):
    '''
    Creates a new task from a form. We assume that the form information is correct.
    '''
    if taskChecker.parentTask is None:
        t = Task(status=False,createdBy=user,description=form['description'].value(),isPrivate=form['private'].value(),title=form['title'].value())
    else:
        t = Task(status=False,createdBy=user,description=form['description'].value(),parent=taskChecker.parentTask,isPrivate=form['private'].value(),title=form['title'].value())

    t.save()

    a = AssignUserToTask(user=user,task=t) #The task is visible to the use who created the task.
    a.save()

    for u in taskChecker.list_of_allowed_users: #Setting task visibility for users
        if User.objects.all().filter(username=u)[0] == user:
            continue
        a = AssignUserToTask(user=(User.objects.filter(username=u)[0]),task=t)
        a.save()

    for tm in taskChecker.list_of_allowed_teams: #Setting team visibility for teams
        a = AssignTeamToTask(team=(Team.objects.filter(name=tm)[0]),task=t)
        a.save()

def deleteAssignments(user, task):
    '''
    Takes a user and a task and deletes all asignments of an user to a task and
    of a team to a task, except for the creator of the task.
    '''
    for userToTaskAssign in AssignUserToTask.objects.filter(task=task):
        if userToTaskAssign != user:
            userToTaskAssign.delete()

    for teamToTaskAssign in AssignTeamToTask.objects.filter(task=task):
        teamToTaskAssign.delete()
        

def updateTask(form, task, taskChecker):
    '''
    Takes a form and a task and updates the task. Assumes the given info
    in the form is valid.
    '''
    task.title = form['title'].value()
    task.description = form['description'].value()
    task.isPrivate = form['private'].value()
    task.save()

    user = task.createdBy

    deleteAssignments(user,task)

    for u in taskChecker.list_of_allowed_users: #Setting task visibility for users
        if User.objects.all().filter(username=u)[0] == user:
            continue
        a = AssignUserToTask(user=(User.objects.filter(username=u)[0]),task=task)
        a.save()

    for tm in taskChecker.list_of_allowed_teams: #Setting team visibility for teams
        a = AssignTeamToTask(team=(Team.objects.filter(name=tm)[0]),task=task)
        a.save()


def get_visible_tasks(user):
    '''
    Returns a list of all tasks that are visible to the given user. 
    '''
    all_tasks = [t for t in Task.objects.all()]
    for t in all_tasks:
        if visibleTask(user,t) == False:
            all_tasks.remove(t) #If non of the above conditions met, the task is removed from the visible tasks list.
    return all_tasks

def visibleTask(user, t):
    '''
    Returns True if a task should be visible to a user.
    A task should be visible to a user if :
    1) The task is doable by the user (see doableTask()).
    or 2) The task is not private.
    '''

    if t.isPrivate == False: #If the task is public.
        return True

    if doableTask(user,t) == True:
        return True
    return False

def doableTaskById(user,task_id):
    '''
    Checks if a user can mark a task as done, the task is given via an id.
    '''
    task = Task.objects.get(id=task_id)
    return doableTask(user,task)

def doableTask(user,task):
    '''
    Checks if a user can mark a task as done. A task can be marked as done by a user if :
    1) The creator of the task is the user.
    or 2) The user is in the list of assigned users to this task.
    or 3) The user is member of a team that is in the list of assigned teams to this task.
    '''
    if(len(AssignUserToTask.objects.filter(user=user,task=task)) >= 1): #If the user is assigned to this task.
        return True

    user_team_assigned_to_task = False
    for assignment in AssignUserToTeam.objects.filter(user=user): #If the user is in a team assigned to this task.
        team = assignment.team
        if(len(AssignTeamToTask.objects.filter(team=team, task=task)) >= 1):
            user_team_assigned_to_task = True
            break
    if(user_team_assigned_to_task == True):
        return True

    if task.createdBy == user: #If the task was created by the user.
        return True
    return False

def doTask(task_id):
    '''
    Takes a task id and marks it as done.
    '''
    task = Task.objects.get(id=task_id)
    task.status = True
    task.save()

def undoTask(task_id):
    '''
    Takes a task id and marks it as undone.
    '''
    task = Task.objects.get(id=task_id)
    task.status = False
    task.save()

def deletableTask(form, user):
    '''
    Checks if a task is deletable by a user, a task should be deletable only by the user
    who created it. This functions returns :
    - True if the task is deletable.
    - False if the task is not deletable.
    - False if the task does not exist.
    '''
    try:
        task = Task.objects.get(id=form['id'].value())
    except Task.DoesNotExist:
        return False
    if(task.createdBy == user):
        return True
    return False

def deleteTask(form):
    '''
    Deletes a task. The task's id is in the form given as parameter. The task given
    in the form must exist else the function will raise a Task.DoesNotExist exception.
    '''
    Task.objects.get(id=form['id'].value()).delete()

def getUsersAssignedToTask(task):
    '''
    Returns all users assigned to this task.
    '''
    assign = AssignUserToTask.objects.filter(task=task)
    return [a.user for a in assign]

def getTeamsAssignedToTask(task):
    '''
    Returns all teams assigned to this task.
    '''
    assign = AssignTeamToTask.objects.filter(task=task)
    return [a.team for a in assign]