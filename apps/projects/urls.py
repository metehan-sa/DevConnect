from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list_view, name='list'),
    path('create/', views.project_create_view, name='create'),
    path('<slug:slug>/', views.project_detail_view, name='detail'),
    path('<slug:slug>/edit/', views.project_update_view, name='edit'),
    path('<slug:slug>/delete/', views.project_delete_view, name='delete'),
    path('<slug:slug>/like/', views.project_toggle_like, name='like'),
    path('<slug:slug>/comment/', views.project_add_comment, name='comment'),
]
