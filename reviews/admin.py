from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'text')
    search_fields = ('user__username', 'text')
    list_filter = ('content_type',)