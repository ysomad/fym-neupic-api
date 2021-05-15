from django.contrib import admin

from .models import Task, Media, App, AppFunction, Subfunction, Bot


class SubfunctionInline(admin.TabularInline):
    model = Subfunction
    extra = 5


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('function', 'bot', 'status', 'created_at')


@admin.register(AppFunction)
class AppFunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'app')
    inlines = [SubfunctionInline]


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'media', 'state', 'uploaded_at')


admin.site.register(App)
admin.site.register(Subfunction)

