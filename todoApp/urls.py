from django.urls import path
from . import views


urlpatterns=[
 path('', views.TaskList, name='menu'),
 path('edit-items/<int:id>/', views.editList, name='edit-items'),
 path('delete/<int:id>/', views.viewdel, name='delete-items'),
 path('detail/<int:id>/',views.detail ,name='items-detail'),
 path('add-item', views.add_item, name='add-items'),
 path('login-user', views.login_user, name='login-user'),
 path('log-out', views.logout_user, name='log-out')
]