from django.contrib import admin

from .models import Task, Media, App, AppFunction, Subfunction, Bot, Config


admin.site.register(Config)


class SubfunctionInline(admin.TabularInline):
    model = Subfunction
    extra = 5


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'function', 'subfunction', 'bot', 'status', 'created_at')
    filter_horizontal = ('media',)
    list_filter = ('function__name', 'subfunction__name', 'status', 'bot')


@admin.register(AppFunction)
class AppFunctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'app')
    inlines = [SubfunctionInline]


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'media', 'type', 'uploaded_at')
    list_filter = ('type', 'tags')


@admin.register(Subfunction)
class SubfunctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'function', 'get_function_app_name')
    list_filter = ('function',)

    def get_function_app_name(self, obj):
        return obj.function.app

    get_function_app_name.short_description = 'app'


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


