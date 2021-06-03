from django.contrib import admin

from .models import Task, Media, App, AppFunction, Subfunction, Bot


class SubfunctionInline(admin.TabularInline):
    model = Subfunction
    extra = 5


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('function', 'bot', 'status', 'created_at')
    filter_horizontal = ('media',)


@admin.register(AppFunction)
class AppFunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'app')
    inlines = [SubfunctionInline]


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'media', 'type', 'uploaded_at')


@admin.register(Subfunction)
class SubfunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'function', 'get_function_app_name')

    def get_function_app_name(self, obj):
        return obj.function.app

    get_function_app_name.short_description = 'app'


admin.site.register(App)

