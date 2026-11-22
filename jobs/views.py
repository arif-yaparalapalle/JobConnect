from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Application
from accounts.models import UserProfile


@login_required(login_url='login')
def post_job_view(request):

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not user_profile or user_profile.role != 'Employer':
        messages.error(request, 'Only Employers can post jobs!')
        return redirect('dashboard')

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        company_name = request.POST.get('company_name', '').strip()
        location = request.POST.get('location', '').strip()
        job_type = request.POST.get('job_type', '').strip()
        salary = request.POST.get('salary', '').strip()
        description = request.POST.get('description', '').strip()

        if not all([title, company_name, location, job_type, salary, description]):
            messages.error(request, 'All Fields Are Required!')
            return redirect('post_job')

        if job_type not in ['Full Time', 'Part Time', 'Internship']:
            messages.error(request, 'Invalid Job Type!')
            return redirect('post_job')

        Job.objects.create(
            posted_by=request.user,
            title=title,
            company_name=company_name,
            location=location,
            job_type=job_type,
            salary=salary,
            description=description
        )

        messages.success(request, 'Job Posted Successfully!')
        return redirect('post_job')

    return render(request, 'post_job.html')
@login_required(login_url='login')
def my_posted_jobs_view(request):

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not user_profile or user_profile.role != 'Employer':
        messages.error(request, 'Only Employers can view posted jobs!')
        return redirect('dashboard')

    jobs = Job.objects.filter(
        posted_by=request.user
    ).order_by('-posted_at')

    return render(
        request,
        'my_posted_jobs.html',
        {'jobs': jobs}
    )
@login_required(login_url='login')
def edit_job_view(request, job_id):

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not user_profile or user_profile.role != 'Employer':
        messages.error(request, 'Only Employers can edit jobs!')
        return redirect('dashboard')

    job = get_object_or_404(
        Job,
        id=job_id,
        posted_by=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        company_name = request.POST.get('company_name', '').strip()
        location = request.POST.get('location', '').strip()
        job_type = request.POST.get('job_type', '').strip()
        salary = request.POST.get('salary', '').strip()
        description = request.POST.get('description', '').strip()

        if not all([title, company_name, location, job_type, salary, description]):
            messages.error(request, 'All Fields Are Required!')
            return redirect('edit_job', job_id=job.id)

        if job_type not in ['Full Time', 'Part Time', 'Internship']:
            messages.error(request, 'Invalid Job Type!')
            return redirect('edit_job', job_id=job.id)

        job.title = title
        job.company_name = company_name
        job.location = location
        job.job_type = job_type
        job.salary = salary
        job.description = description

        job.save()

        messages.success(request, 'Job Updated Successfully!')
        return redirect('my_posted_jobs')

    return render(
        request,
        'edit_job.html',
        {'job': job}
    )
@login_required(login_url='login')
def employer_applications_view(request):

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not user_profile or user_profile.role != 'Employer':
        messages.error(request, 'Only Employers can view applications!')
        return redirect('dashboard')

    applications = Application.objects.filter(
        job__posted_by=request.user
    ).select_related('job', 'applicant').order_by('-applied_at')

    return render(
        request,
        'employer_applications.html',
        {'applications': applications}
    )
@login_required(login_url='login')
def update_application_status_view(request, application_id):

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not user_profile or user_profile.role != 'Employer':
        messages.error(request, 'Only Employers can update application status!')
        return redirect('dashboard')

    application = get_object_or_404(
        Application,
        id=application_id,
        job__posted_by=request.user
    )

    if request.method == 'POST':

        status = request.POST.get('status')

        if status in ['Pending', 'Accepted', 'Rejected']:

            application.status = status
            application.save()

            messages.success(request, 'Application status updated successfully!')

        else:
            messages.error(request, 'Invalid application status!')

    return redirect('employer_applications')
@login_required(login_url='login')
def delete_job_view(request, job_id):

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not user_profile or user_profile.role != 'Employer':
        messages.error(request, 'Only Employers can delete jobs!')
        return redirect('dashboard')

    job = get_object_or_404(
        Job,
        id=job_id,
        posted_by=request.user
    )

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job Deleted Successfully!')
        return redirect('my_posted_jobs')

    return render(
        request,
        'delete_job.html',
        {'job': job}
    )
def job_list_view(request):

    jobs = Job.objects.filter(is_active=True).order_by('-posted_at')

    search = request.GET.get('search')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')

    if search:
        jobs = jobs.filter(title__icontains=search)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    return render(
        request,
        'job_list.html',
        {
            'jobs': jobs,
            'search': search,
            'location': location,
            'job_type': job_type
        }
    )
@login_required(login_url='login')
def apply_job_view(request, job_id):

    if request.method != 'POST':
        return redirect('job_list')

    job = get_object_or_404(Job, id=job_id)

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not user_profile or user_profile.role != 'Job Seeker':
        messages.error(request, 'Only Job Seekers can apply for jobs!')
        return redirect('dashboard')

    application, created = Application.objects.get_or_create(
        job=job,
        applicant=request.user
    )

    if created:
        messages.success(request, 'Job Application Submitted Successfully!')
    else:
        messages.warning(request, 'You have already applied for this job!')

    return redirect('job_list')
@login_required(login_url='login')
def my_applications_view(request):

    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job').order_by('-applied_at')

    return render(
        request,
        'my_applications.html',
        {'applications': applications}
    )