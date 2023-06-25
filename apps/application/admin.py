from django.contrib import admin
from apps.application.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass
