from django.contrib import admin

from .models import Advertisement


@admin.register(Advertisement)
class AAdmin(admin.ModelAdmin):
    pass
