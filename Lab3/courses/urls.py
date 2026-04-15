from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('new/', views.course_create, name='course_create'),
    path('api/courses/<int:pk>/', views.api_course_detail, name='api_course_detail'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('api/courses/', views.api_courses, name='api_courses'),
    path('category/<int:pk>/', views.category_detail, name='category_detail')
]
