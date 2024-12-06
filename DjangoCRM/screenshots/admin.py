from django.contrib import admin
from .models import Screenshot

@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at')
    ordering = ('-uploaded_at',)
