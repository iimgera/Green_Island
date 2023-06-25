from django.contrib import admin
from apps.home.models import (
    Point, Section, 
    Rules, Contact,
    Category,
)    


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Section)
class SectoonAdmin(admin.ModelAdmin):
    pass


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
