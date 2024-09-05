# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from apps.home import views
from .views import customer_list, customer_create, customer_update, customer_delete, customer_contact_detail, \
    create_contact, delete_contact

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('dep_develop/', views.dep_develop, name='dep_develop'),
    path('get_daily_items/', views.get_daily_items, name='get_daily_items'),
    path('dep_develop/create/', views.dep_develop_create_project, name='dep_develop_create_project'),
    path('dep_develop/edit/', views.dep_develop_edit_project, name='dep_develop_edit_project'),

    path('dep_business/', views.dep_business, name='dep_business'),
    path('dep_business/create/', views.dep_business_create_project, name='dep_business_create_project'),
    path('dep_business/edit/', views.dep_business_edit_project, name='dep_business_edit_project'),

    path('dep_tech/', views.dep_tech, name='dep_tech'),
    path('dep_tech/create/', views.dep_tech_create_project, name='dep_tech_create_project'),
    path('dep_tech/edit/', views.dep_tech_edit_project, name='dep_tech_edit_project'),

    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),

    path('submit_gpa/', views.submit_gpa, name='submit_gpa'),

    path('daily/', views.daily, name='daily'),
    path('daily/add/', views.daily_add, name='daily_add'),

    path('profile/', views.profile, name='profile'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

    path('customers/', customer_list, name='customer-list'),
    path('customer/create/', customer_create, name='customer-create'),
    path('customer/update/', customer_update, name='customer-update'),
    path('customer/delete/', customer_delete, name='customer-delete'),
    path('customers/', customer_list, name='customer-list'),
    path('customer/<int:customer_id>/contact/', customer_contact_detail, name='customer-contact-detail'),
    path('customer/<int:customer_id>/contact/create/', create_contact, name='customer-contact-create'),
    path('customer/<int:customer_id>/contact/delete/', delete_contact, name='customer-contact-delete'),
]
