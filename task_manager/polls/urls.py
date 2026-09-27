from django.urls import path

#from django.conf import  settings
#from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path("sign_out/", views.sign_out, name="sign_out"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/create_tasks", views.create_tasks, name="create_tasks"),
    path("tasks/create_tasks/<int:parent_id>", views.create_subtasks, name="create_subtasks"),
    path("tasks/update_tasks/<int:task_id>", views.update_tasks, name="update_tasks"),
    path("tasks/delete_tasks", views.delete_tasks, name="delete_tasks"),
    path("tasks/do_tasks/<int:task_id>", views.do_tasks, name="do_tasks"),
    path("tasks/undo_tasks/<int:task_id>", views.undo_tasks, name="undo_tasks"),
    path("tasks/<int:task_id>", views.task_inspect, name="task_inspect"),
    path("user/<int:user_id>", views.users, name="users"),
    path("teams/", views.teams, name="teams"),
    path("teams/create_teams", views.create_teams, name="create_teams"),
    path("teams/join_teams/<str:team_name>", views.join_teams, name="join_teams"),
    path("teams/leave_teams/<str:team_name>", views.leave_teams, name="leave_teams"),
    path("teams/delete_teams/<str:team_name>",views.delete_teams,name="delete_teams"),
    path("teams/<str:team_name>",views.team_inspect,name="team_inspect"),
    path("",views.index, name="index")
]