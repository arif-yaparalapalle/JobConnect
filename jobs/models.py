from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):

    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Application(models.Model):

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"  