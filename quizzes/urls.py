from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),# home page 
    path('dashboard', views.dashboard, name='dashboard'), # dashboard
    path('<int:quiz_id>/', views.quiz_info, name='quiz_info'),
    path('<int:quiz_id>/create_score/', views.create_score),
    path('<int:quiz_id>/result', views.result),
    path('<int:quiz_id>/save_result', views.save_result),
]