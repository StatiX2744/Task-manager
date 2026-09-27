from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Team)
admin.site.register(User)
admin.site.register(Task)
admin.site.register(AssignTeamToTask)
admin.site.register(AssignUserToTask)
