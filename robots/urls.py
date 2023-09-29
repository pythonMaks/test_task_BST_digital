from django.urls import path
from robots.views import create_robot, export_excel

urlpatterns = [
    path('create_robot/', create_robot, name='create_robot'),
    path('export_excel/', export_excel, name='export_excel'),
]
