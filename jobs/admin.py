from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'company_name',
        'location',
        'job_type',
        'salary',
        'is_active',
        'posted_at'
    )

    list_filter = ('job_type', 'is_active')

    search_fields = ('title', 'company_name', 'location')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'applicant',
        'job',
        'applied_at',
        'status'
    )

    list_filter = ('status', 'applied_at')

    search_fields = ('applicant__username', 'job__title')