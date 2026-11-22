from django.urls import path
from . import views

urlpatterns = [
    path('post-job/', views.post_job_view, name='post_job'),
    path('my-posted-jobs/', views.my_posted_jobs_view, name='my_posted_jobs'),
    path('employer-applications/', views.employer_applications_view, name='employer_applications'),
    path('update-application-status/<int:application_id>/', views.update_application_status_view, name='update_application_status'),
    path('edit-job/<int:job_id>/', views.edit_job_view, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job_view, name='delete_job'),
    path('jobs/', views.job_list_view, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job_view, name='apply_job'),
    path('my-applications/', views.my_applications_view, name='my_applications'),
]