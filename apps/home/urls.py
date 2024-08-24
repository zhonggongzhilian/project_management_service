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
    path('dep_develop/create/', views.dep_develop_create_project, name='dep_develop_create_project'),
    path('dep_develop/edit/', views.dep_develop_edit_project, name='dep_develop_edit_project'),

    path('daily/', views.daily, name='daily'),
    path('daily/add/', views.daily_add, name='daily_add'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
