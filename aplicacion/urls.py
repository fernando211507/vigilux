from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_rule, name='create_rule'),
    path('list/', views.rule_list, name='rule_list'),
    path('', views.ping_list, name='ping_list'), 
    path('dns-lookup/', views.dns_lookup, name='dns_lookup'),
    path('dns-result/<int:pk>/', views.dns_result, name='dns_result'),
    path('admin/informes/', views.informes, name='informes'),
]
