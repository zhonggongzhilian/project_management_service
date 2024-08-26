# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import date

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from .models import Daily, GPA, DailyItem
from .models import Project


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
    projects = Project.objects.filter(department=1)
    users = User.objects.all()
    for project in projects:
        daily_item = DailyItem.objects.filter(project=project).first()
        project.description = daily_item.description
    return render(request, 'home/dep_develop.html', {'projects': projects, 'users': users})


@login_required(login_url="/login/")
def get_daily_items(request):
    project_id = request.GET.get('project_id')
    daily_items = DailyItem.objects.filter(project_id=project_id).values('date', 'description')
    return JsonResponse(list(daily_items), safe=False)


@login_required(login_url="/login/")
def dep_develop_create_project(request):
    if request.method == 'POST':
        name = request.POST['name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        priority = request.POST['priority']
        owner_ids = request.POST.getlist('owner')
        owners = User.objects.filter(id__in=owner_ids)

        project = Project.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            status=status,
            priority=priority,
            department=1
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
def dep_business(request):
    projects = Project.objects.filter(department=2)
    users = User.objects.all()
    for project in projects:
        daily_item = DailyItem.objects.filter(project=project).first()
        project.description = daily_item.description
    for project in projects:
        daily_item = DailyItem.objects.filter(project=project).first()
        project.description = daily_item.description
    return render(request, 'home/dep_business.html', {'projects': projects, 'users': users})


@login_required(login_url="/login/")
def dep_business_create_project(request):
    if request.method == 'POST':
        name = request.POST['name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        priority = request.POST['priority']
        owner_ids = request.POST.getlist('owner')
        owners = User.objects.filter(id__in=owner_ids)

        project = Project.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            status=status,
            priority=priority,
            department=2
        )
        project.owner.set(owners)
        project.save()

        return redirect('dep_business')  # 重定向到项目列表页面

    return redirect('dep_business')


@login_required(login_url="/login/")
def dep_business_edit_project(request):
    if request.method == 'POST':
        project_id = request.POST['id']
        project = get_object_or_404(Project, id=project_id)

        project.name = request.POST['name']
        project.start_date = request.POST['start_date']
        project.end_date = request.POST['end_date']
        project.status = request.POST['status']
        project.priority = request.POST['priority']

        owner_ids = request.POST.getlist('owner')
        owners = User.objects.filter(id__in=owner_ids)
        project.owner.set(owners)

        project.save()
        return redirect('dep_business')

    return redirect('dep_business')


@login_required(login_url="/login/")
def dep_tech(request):
    projects = Project.objects.filter(department=3)
    users = User.objects.all()
    for project in projects:
        daily_item = DailyItem.objects.filter(project=project).first()
        project.description = daily_item.description
    return render(request, 'home/dep_tech.html', {'projects': projects, 'users': users})


@login_required(login_url="/login/")
def dep_tech_create_project(request):
    if request.method == 'POST':
        name = request.POST['name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        priority = request.POST['priority']
        owner_ids = request.POST.getlist('owner')
        owners = User.objects.filter(id__in=owner_ids)

        project = Project.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            status=status,
            priority=priority,
            department=3
        )
        project.owner.set(owners)
        project.save()

        return redirect('dep_tech')  # 重定向到项目列表页面

    return redirect('dep_tech')


@login_required(login_url="/login/")
def dep_tech_edit_project(request):
    if request.method == 'POST':
        project_id = request.POST['id']
        project = get_object_or_404(Project, id=project_id)

        project.name = request.POST['name']
        project.start_date = request.POST['start_date']
        project.end_date = request.POST['end_date']
        project.status = request.POST['status']
        project.priority = request.POST['priority']

        owner_ids = request.POST.getlist('owner')
        owners = User.objects.filter(id__in=owner_ids)
        project.owner.set(owners)

        project.save()
        return redirect('dep_tech')

    return redirect('dep_tech')


@login_required(login_url="/login/")
def daily(request):
    daily_reports = Daily.objects.all()  # 或者你可以根据需要筛选日报
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'home/daily.html', {'daily_reports': daily_reports,
                                               'projects': projects})


@login_required(login_url="/login/")
def daily_add(request):
    if request.method == 'POST':
        today = date.today()

        content = request.POST.get('content')
        projects = request.POST.getlist('projects[]')
        descriptions = request.POST.getlist('descriptions[]')

        # Check if there's already a Daily entry for today
        existing_daily = Daily.objects.filter(user_profile=request.user.userprofile, date=today).first()

        if existing_daily:
            # Delete existing DailyItems
            DailyItem.objects.filter(daily=existing_daily).delete()
            # Delete the existing Daily entry
            existing_daily.delete()

        # Create Daily instance
        daily = Daily.objects.create(
            user_profile=request.user.userprofile,
            date=today,  # Or any other date
            content=content
        )

        # Create DailyItems
        for project_id, description in zip(projects, descriptions):
            project = Project.objects.get(id=project_id)
            DailyItem.objects.create(
                daily=daily,
                project=project,
                description=description,
                date=today
            )
        return redirect('daily')  # Redirect to the daily reports page

    return redirect('daily')  # In case of GET request or invalid request


@login_required(login_url="/login/")
def profile(request):
    daily_reports = Daily.objects.all()  # 或者你可以根据需要筛选日报
    gpas = GPA.objects.filter(user=request.user)  # 查询当前用户的所有 GPA 数据
    return render(request, 'home/profile.html', {
        'daily_reports': daily_reports,
        'gpas': gpas,
    })


@login_required
def submit_gpa(request):
    if request.method == 'POST':
        item = request.POST.get('item')
        value = float(request.POST.get('value'))
        desc = request.POST.get('desc')

        # 创建新的 GPA 对象
        gpa = GPA(
            item=item,
            value=value,
            desc=desc,
            is_approved=False,
            user=request.user
        )
        gpa.save()

        # 你可以返回 JSON 响应以处理 AJAX 请求
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
