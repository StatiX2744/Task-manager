from .forms import CreateTaskForm
from .models import User, Team, Task, AssignUserToTask, AssignTeamToTask, AssignUserToTeam
from .TaskChecker import TaskChecker


def getAllTeams():
    '''
    Returns all the existing teams. 
    '''
    return Team.objects.all()

def joinableTeam(user, team_name):
    '''
    Returns a boolean if the user can join the team.
    A team is joinable if the user is not already in a
    team, and if the team with this id exists.
    '''
    try:
        team = Team.objects.get(name=team_name)
    except Team.DoesNotExist:
        return False
    
    try:
        assign = AssignUserToTeam.objects.get(user=user,team=team)
    except:
        return True
    return False

def joinTeam(user,team_name):
    '''
    Makes a user join a team, we suppose that the team exists.
    '''
    team = Team.objects.get(name=team_name)
    assign = AssignUserToTeam(user=user,team=team)
    assign.save()

def leavableTeam(user,team_name):
    '''
    Checks if a team is leavable by a user.
    '''
    try:
        team = Team.objects.get(name=team_name)
    except Team.DoesNotExist:
        return False
    
    try:
        assign = AssignUserToTeam.objects.get(user=user,team=team)
    except:
        return False
    return True

def leaveTeam(user,team):
    '''
    Makes a user leave the team, we suppose that the user is in
    the team.
    '''
    assign = AssignUserToTeam.objects.get(user=user,team=team)
    assign.delete()
    

def createTeam(user, name):
    '''
    Creates a new team with the given name.
    '''
    team = Team(name=name,createdBy=user)
    team.save()

def deleteTeam(team):
    '''
    Deletes the given team.
    '''
    team.delete()

def teamValidityChecker(name):
    '''
    Checks the validity of a team name, a team
    name is valid iff a team with that exact name
    does not already exist.
    '''
    try:
        Team.objects.get(name=name)
    except:
        return True
    return False

def getTeamFromName(team_name):
    '''
    Returns the team corresponding to the team name
    given.
    '''
    return Team.objects.get(name=team_name)

def getTeamMembers(team):
    '''
    Returns the team's members.
    '''
    assign = AssignUserToTeam.objects.filter(team=team)
    return [a.user for a in assign]

def getTeamTasks(team):
    '''
    Returns the team's tasks.
    '''
    assign = AssignTeamToTask.objects.filter(team=team)
    return [a.task for a in assign]