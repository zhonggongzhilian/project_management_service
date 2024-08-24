# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse

from .models import Project, Daily, UserProfile

from datetime import date

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def dep_develop(request):
    projects = Project.objects.all()
    users = User.objects.all()
    return render(request, 'home/dep_develop.html', {'projects': projects, 'users': users})


@login_required(login_url="/login/")
def dep_develop_create_project(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        priority = request.POST['priority']
        owner_ids = request.POST.getlist('owner')
        owners = User.objects.filter(id__in=owner_ids)

        project = Project.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            status=status,
            priority=priority,
        )
        project.owner.set(owners)
        project.save()

        return redirect('dep_develop')  # 重定向到项目列表页面

    return redirect('dep_develop')


@login_required(login_url="/login/")
def dep_develop_edit_project(request):
    if request.method == 'POST':
        project_id = request.POST['id']
        project = get_object_or_404(Project, id=project_id)

        project.name = request.POST['name']
        project.description = request.POST.get('description', '')
        project.start_date = request.POST['start_date']
        project.end_date = request.POST['end_date']
        project.status = request.POST['status']
        project.priority = request.POST['priority']

        owner_ids = request.POST.getlist('owner')
        owners = User.objects.filter(id__in=owner_ids)
        project.owner.set(owners)

        project.save()
        return redirect('dep_develop')

    return redirect('dep_develop')


@login_required(login_url="/login/")
def daily(request):
    daily_reports = Daily.objects.all()  # 或者你可以根据需要筛选日报
    return render(request, 'home/daily.html', {'daily_reports': daily_reports})


@login_required(login_url="/login/")
def daily_add(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        today = date.today()
        user_profile = UserProfile.objects.filter(user=request.user).first()

        # Create or update daily report
        Daily.objects.update_or_create(
            user_profile=user_profile,
            date=today,
            defaults={'content': content}
        )
        return redirect('daily')  # Redirect to the daily reports page

    return redirect('daily')  # In case of GET request or invalid request
