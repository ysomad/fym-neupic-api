from django.contrib import admin

from .models import Task, TaskData, App, AppFunction, Subfunction, Bot


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('data', 'bot', 'status')


@admin.register(AppFunction)
class AppFunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'app')


admin.site.register(TaskData)
admin.site.register(App)
admin.site.register(Subfunction)
admin.site.register(Bot)