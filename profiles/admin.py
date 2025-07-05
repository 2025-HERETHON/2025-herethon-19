from django.contrib import admin
from .models import MentorVerification

# Register your models here.

@admin.register(MentorVerification)
class MentorVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified', 'is_skipped']
    list_filter = ['is_verified', 'is_skipped']
    search_fields = ['user__email']