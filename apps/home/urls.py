# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from apps.home import views

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

    path('submit_gpa/', views.submit_gpa, name='submit_gpa'),

    path('daily/', views.daily, name='daily'),
    path('daily/add/', views.daily_add, name='daily_add'),

    path('profile/', views.profile, name='profile'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
