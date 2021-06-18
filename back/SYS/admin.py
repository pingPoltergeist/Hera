from django.contrib import admin
from .models import System


# Register your models here.
class SystemAdmin(admin.ModelAdmin):
    meta = System
    list_display = ['key', 'value']


admin.site.register(System, SystemAdmin)
