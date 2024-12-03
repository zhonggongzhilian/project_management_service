# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import date, datetime

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Customer, UserProfile
from .models import Daily, GPA, DailyItem, Department, CustomerContact
from .models import Project, ProjectType
from ..authentication.forms import CustomerForm, CustomerContactForm
from apps.authentication.forms  import PasswordChangeForm

@login_required(login_url="/login/")
def index(request):
    users = User.objects.all()
    user_amount = len(users)
    projects = Project.objects.all()
    project_amount = len(projects)

    clients = Customer.objects.all()

    total_amount = 0
    for project in projects:
        if project.status == 'completed':
            total_amount += project.amount

    dailies = Daily.objects.all()
    daily_amount = len(dailies)

    from django.utils import timezone

    # 获取今天的日期
    today = timezone.now().date()

    # 计算今天的日报数量
    dailies_today = Daily.objects.filter(date=today)
    daily_amount_today = len(dailies_today)

    project_data = []
    for project in projects:
        start_date = project.start_date
        end_date = project.end_date
        total_days = (end_date - start_date).days
        elapsed_days = (today - start_date).days
        progress_percentage = (elapsed_days / total_days) * 100 if total_days > 0 else 0

        project_data.append({
            'type': project.project_type.name,
            'name': project.name,
            'responsible': project.owner,
            'progress': round(progress_percentage, 2),
        })

    from django.db.models import Sum
    sales_data = []
    business_users = User.objects.filter(userprofile__department__id=2)
    for user in business_users:
        total_amount = \
        Project.objects.filter(owner=user, is_approved=1, department=2).aggregate(total_amount=Sum('amount'))[
            'total_amount'] or 0
        sales_data.append({
            'username': user.username,
            'total_amount': total_amount,
        })

    # 按总销售额排序
    sales_data.sort(key=lambda x: x['total_amount'], reverse=True)

    # 计算百分比
    if user_amount != 0:
        progress_percentage = (daily_amount_today / user_amount) * 100
    else:
        progress_percentage = 0

    context = {'user_amount': user_amount,
               'project_amount': project_amount,
               'progress_percentage': round(progress_percentage, 2),
               'total_amount': total_amount,
               'daily_amount': daily_amount,
               'daily_amount_today': daily_amount_today,
               'project_data': project_data,
               'sales_data': sales_data,
               'clients': clients,
               }

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
    # 获取所有用户以供选择
    users = User.objects.filter(userprofile__department__id=1)
    clients = Customer.objects.all()

    # 获取查询参数
    selected_user_id = request.GET.get('user')

    if request.user.is_superuser:
        # 管理员可以查看所有项目，如果有选择用户则过滤项目
        if selected_user_id:
            projects = Project.objects.filter(department=1, owner_id=selected_user_id).order_by('end_date')
        else:
            projects = Project.objects.filter(department=1).order_by('end_date')
    else:
        # 非管理员用户只能查看自己负责的项目
        projects = Project.objects.filter(owner=request.user, department=1).order_by('end_date')

    project_types = ProjectType.objects.filter(department=1)

    for project in projects:
        daily_item = DailyItem.objects.filter(project=project).last()
        project.description = daily_item.description if daily_item else ""

    context = {
        'projects': projects,
        'users': users,
        'project_types': project_types,
        'clients': clients,
    }

    return render(request, 'home/dep_develop.html',
                  context=context)


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
        project_type = ProjectType.objects.get(id=request.POST['project_type'])
        owner = User.objects.get(id=request.POST['owner'])
        client = Customer.objects.get(id=request.POST['client'])
        department = Department.objects.get(id=1)

        project = Project.objects.create(
            name=name,
            project_type=project_type,
            start_date=start_date,
            end_date=end_date,
            status=status,
            department=department,
            owner=owner,
            client=client
        )
        project.save()

        return redirect('dep_develop')  # 重定向到项目列表页面

    return redirect('dep_develop')


@login_required(login_url="/login/")
def dep_develop_edit_project(request):
    if request.method == 'POST':
        project_id = request.POST['id']
        project = get_object_or_404(Project, id=project_id)

        project.name = request.POST['name']
        project.status = request.POST['status']
        project.progress = request.POST['progress']

        project_type = get_object_or_404(ProjectType, id=request.POST['projecttype'])
        owner = get_object_or_404(User, id=request.POST['owner'])
        client = Customer.objects.get(id=request.POST['client'])

        project.project_type = project_type
        project.owner = owner
        project.client = client

        project.save()
        return redirect('dep_develop')

    return redirect('dep_develop')

@login_required(login_url="/login/")
def submit_project_for_approval(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)

        # 确保进度为100%
        if project.progress == 100:
            project.is_approved = False  # 设置为待审核状态
            project.save()
            return JsonResponse({'success': True, 'message': '项目已提交审核'})

    return JsonResponse({'success': False, 'message': '提交审核失败'})


@login_required(login_url="/login/")
def approve_project(request, project_id):
    if request.method == 'POST' and request.user.is_superuser:
        project = get_object_or_404(Project, id=project_id)

        if project.progress == 100:
            project.is_approved = True
            project.save()
            return JsonResponse({'success': True, 'message': '项目已审核通过'})

    return JsonResponse({'success': False, 'message': '审核失败'})

@login_required(login_url="/login/")
def return_project_for_modification(request, project_id):
    if request.method == 'POST' and request.user.is_superuser:
        project = get_object_or_404(Project, id=project_id)

        # 将审核状态设置为未通过，并且项目进度可以保留为100%
        if project.is_approved:
            project.is_approved = False
            project.save()
            return JsonResponse({'success': True, 'message': '项目已退回修改'})

    return JsonResponse({'success': False, 'message': '退回修改失败'})

@login_required(login_url="/login/")
def submit_review(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        if project.status == 'completed':
            project.is_approved = False  # 标记为待审核状态
            project.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@login_required(login_url="/login/")
def approve_project(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        if project.status == 'completed':
            project.is_approved = True  # 标记为审核通过
            project.status = '已审核'  # 状态改为已审核
            project.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@login_required(login_url="/login/")
def return_edit(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        if project.status == '已审核' and project.is_approved:
            project.is_approved = False  # 返回修改，标记为未审核状态
            project.status = '已完成'  # 状态改回已完成，允许再次提交审核
            project.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required(login_url="/login/")
def dep_business(request):
    # 获取所有用户以供选择
    users = User.objects.filter(userprofile__department__id=2)

    # 获取所有客户列表
    clients = Customer.objects.all()

    # 获取查询参数
    selected_user_id = request.GET.get('user')

    if request.user.is_superuser:
        # 管理员可以查看所有项目，如果有选择用户则过滤项目
        if selected_user_id:
            projects = Project.objects.filter(department=2, owner_id=selected_user_id).order_by('end_date')
        else:
            projects = Project.objects.filter(department=2).order_by('end_date')
    else:
        # 非管理员用户只能查看自己负责的项目
        projects = Project.objects.filter(owner=request.user, department=2).order_by('end_date')

    project_types = ProjectType.objects.filter(department=2)

    for project in projects:
        daily_item = DailyItem.objects.filter(project=project).first()
        project.description = daily_item.description if daily_item else ""

    return render(request, 'home/dep_business.html', {
        'projects': projects,
        'users': users,
        'project_types': project_types,
        'clients': clients,
        'selected_user': selected_user_id,  # 将选择的用户ID传递回模板
    })


@login_required(login_url="/login/")
def dep_business_create_project(request):
    if request.method == 'POST':
        name = request.POST['name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        amount = request.POST['amount']
        owner = request.user
        project_type = ProjectType.objects.get(id=request.POST['project_type'])
        department = Department.objects.get(id=2)

        project = Project.objects.create(
            name=name,
            project_type=project_type,
            start_date=start_date,
            end_date=end_date,
            status=status,
            department=department,
            owner=owner,
            amount=amount
        )
        project.save()

        return redirect('dep_business')  # 重定向到项目列表页面

    return redirect('dep_business')


@login_required(login_url="/login/")
def dep_business_edit_project(request):
    if request.method == 'POST':
        project_id = request.POST['id']
        project = get_object_or_404(Project, id=project_id)
        project_type = get_object_or_404(ProjectType, id=request.POST['project_type'])
        owner = get_object_or_404(User, id=request.POST['owner'])
        client = get_object_or_404(Customer, id=request.POST['client'])  # 添加这行代码，确保 client 定义正确
        project.name = request.POST['name']
        project.status = request.POST['status']
        project.amount = request.POST['amount']
        project.project_type = project_type
        project.owner = owner
        project.client = client  # 确保更新客户信息

        project.save()
        return redirect('dep_business')

    return redirect('dep_business')

@login_required(login_url="/login/")
def dep_tech_create_project(request):
    if request.method == 'POST':
        name = request.POST['name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        amount = 0
        owner = request.user
        project_type = ProjectType.objects.get(id=request.POST['project_type'])
        department = Department.objects.get(id=3)
        client_id = request.POST.get('client', None)
        client = Customer.objects.get(id=client_id) if client_id else None

        project = Project.objects.create(
            name=name,
            project_type=project_type,
            start_date=start_date,
            end_date=end_date,
            status=status,
            department=department,
            owner=owner,
            amount=amount,
            client=client
        )
        project.save()

        return redirect('dep_tech')  # 重定向到项目列表页面

    return redirect('dep_tech')


@login_required(login_url="/login/")
def dep_tech_edit_project(request):
    if request.method == 'POST':
        project_id = request.POST['id']
        project = get_object_or_404(Project, id=project_id)

        project.name = request.POST['name']
        project.status = request.POST['status']
        project.progress = request.POST['progress']
        client_id = request.POST.get('client', None)
        project.client = Customer.objects.get(id=client_id) if client_id else None

        project.save()
        return redirect('dep_tech')

    return redirect('dep_tech')


@login_required(login_url="/login/")
def dep_tech(request):
    if request.user.is_superuser:
        projects = Project.objects.filter(department=3)
        users = User.objects.all()
    else:
        projects = Project.objects.filter(owner=request.user, department=3)
        users = User.objects.filter(username=request.user.username)

    project_types = ProjectType.objects.filter(department=3)
    customers = Customer.objects.all()  # 传递客户列表

    for project in projects:
        daily_item = DailyItem.objects.filter(project=project).first()
        project.description = daily_item.description if daily_item else ""

    return render(request, 'home/dep_tech.html', {'projects': projects, 'users': users, 'project_types': project_types, 'customers': customers})


@login_required(login_url="/login/")
def daily(request):
    # 获取所有日报
    daily_reports = Daily.objects.all()

    # 获取所有项目
    projects = Project.objects.filter(owner=request.user)

    # 按部门对日报进行分组
    daily_reports_by_department = {}
    for daily_report in daily_reports:
        department = daily_report.user_profile.department
        if department not in daily_reports_by_department:
            daily_reports_by_department[department] = []
        daily_reports_by_department[department].append(daily_report)

    # 准备传递给模板的数据
    context = {
        'daily_reports_by_department': daily_reports_by_department,
        'projects': projects,
    }

    return render(request, 'home/daily.html', context)

@login_required
def delete_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        # 检查权限，如果需要确保当前用户有权限删除项目
        if request.user.is_superuser or project.owner == request.user:
            project.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': '没有权限删除此项目'})
    return JsonResponse({'success': False, 'error': '无效的请求'})


@login_required(login_url="/login/")
def daily_add(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        projects = request.POST.getlist('projects[]')
        descriptions = request.POST.getlist('descriptions[]')
        date_str = request.POST.get('date')  # Get the date string from the form
        date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert the date string to a datetime.date object

        # Check if there's already a Daily entry for the selected date
        existing_daily = Daily.objects.filter(user_profile=request.user.userprofile, date=date).first()

        if existing_daily:
            # Delete existing DailyItems
            DailyItem.objects.filter(daily=existing_daily).delete()
            # Delete the existing Daily entry
            existing_daily.delete()

        # Create Daily instance
        daily = Daily.objects.create(
            user_profile=request.user.userprofile,
            date=date,  # Use the selected date
            content=content
        )

        # Create DailyItems
        for project_id, description in zip(projects, descriptions):
            project = Project.objects.get(id=project_id)
            DailyItem.objects.create(
                daily=daily,
                project=project,
                description=description,
                date=date
            )
        return redirect('daily')  # Redirect to the daily reports page

    return redirect('daily')  # In case of GET request or invalid request


@login_required(login_url="/login/")
def profile(request):
    # 检查用户是否是超级用户
    is_superuser = request.user.is_superuser

    # 获取当前用户的未批准且状态为 completed 的项目
    incomplete_projects = None
    if is_superuser:
        incomplete_projects = Project.objects.filter(
            owner=request.user,
            is_approved=False,
            status='completed'
        )

    my_projects = Project.objects.filter(owner=request.user)

    # 获取所有部门，用于下拉菜单选择
    departments = Department.objects.all()

    if request.method == 'POST':
        # 用户提交了部门修改请求
        new_department_id = request.POST.get('department')
        if new_department_id:
            try:
                new_department = Department.objects.get(id=new_department_id)
                user_profile = request.user.userprofile
                user_profile.department = new_department
                user_profile.save()
                messages.success(request, '部门已成功更新。')
            except Department.DoesNotExist:
                messages.error(request, '所选部门不存在。')
        else:
            messages.error(request, '请选择一个部门。')

    return render(request, 'home/profile.html', {
        'incomplete_projects': incomplete_projects,
        'my_projects': my_projects,
        'is_superuser': is_superuser,
        'departments': departments
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

@login_required(login_url="/login/")
def customer_list(request):
    search_query = request.GET.get('search')
    customers = Customer.objects.all()
    business_members = UserProfile.objects.filter(department_id=2)
    if search_query:
        customers = customers.filter(name__icontains=search_query)

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer-list')
    else:
        form = CustomerForm()

    return render(request, 'home/customers.html', {'customers': customers, 'form': form, 'business_members': business_members})


@login_required(login_url="/login/")
def customer_create(request):
    business_members = UserProfile.objects.filter(department_id=2)
    print(len(business_members))  # 检查商务部成员的数量

    # 打印 SQL 查询
    print(connection.queries[-1]['sql'])

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer-list')
    else:
        form = CustomerForm()
    return render(request, 'home/customer_form.html', {'form': form, 'business_members': business_members})


@login_required(login_url="/login/")
def customer_update(request):
    if request.method == 'POST':
        customer_id = request.POST.get('id')
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer-list')
    else:
        customer_id = request.GET.get('id')
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerForm(instance=customer)
    return render(request, 'home/customer_form.html', {'form': form})


@require_POST
@csrf_exempt
def customer_delete(request):
    customer_id = request.POST.get('customer_id')
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return JsonResponse({'success': True})
        except Customer.DoesNotExist:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})


def customer_contact_detail(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    contacts = customer.contacts.all()
    return render(request, 'home/customer_contact_detail.html', {'customer': customer, 'contacts': contacts})


# 新建联系人
@require_POST
def create_contact(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    form = CustomerContactForm(request.POST)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.customer = customer
        contact.save()
        return redirect('customer-contact-detail', customer_id=customer_id)
    else:
        return render(request, 'home/customer_contact_detail.html',
                      {'customer': customer, 'contacts': customer.contacts.all(), 'form': form})


@require_POST
@csrf_exempt
def delete_contact(request, customer_id):
    contact_id = request.POST.get('contact_id')
    contact = get_object_or_404(CustomerContact, pk=contact_id)
    contact.delete()
    return redirect('customer-contact-detail', customer_id=customer_id)



# 定义公司内部验证码（假设为固定值）
COMPANY_VERIFICATION_CODE = 'ZGZL@8888'  # 请将此处替换为您的公司验证码

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            verification_code = form.cleaned_data.get('verification_code')
            new_password = form.cleaned_data.get('new_password')

            # 验证公司内部验证码
            if verification_code != COMPANY_VERIFICATION_CODE:
                messages.error(request, '公司内部验证码不正确。')
                return render(request, 'home/change_password.html', {'form': form})

            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, '密码已成功修改，请使用新密码登录。')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, '用户名不存在。')
    else:
        form = PasswordChangeForm()
    return render(request, 'home/change_password.html', {'form': form})
