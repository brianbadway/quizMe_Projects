from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),# home page 
    path('dashboard', views.dashboard, name='dashboard'), # dashboard
    path('<int:quiz_id>/', views.quiz_info, name='quiz_info'),
    path('<int:quiz_id>/create_score/', views.create_score),
    path('<int:quiz_id>/result', views.result),
    path('<int:quiz_id>/save_result', views.save_result),
    path('<int:quiz_id>/<int:result_id>', views.retake_quiz_info),
    path('<int:quiz_id>/new_score/<int:result_id>', views.new_score),
    path('<int:quiz_id>/<int:result_id>/new_result', views.new_result),
    path('<int:quiz_id>/<int:result_id>/overwrite_result', views.overwrite_result),
    path('new_quiz', views.new_quiz),
    path('create_quiz', views.create_quiz),
    path('<int:quiz_id>/new_question', views.new_question),
    path('<int:quiz_id>/create_question', views.create_question),
    path('<int:quiz_id>/<int:question_id>/new_answer', views.new_answer),
    path('<int:quiz_id>/<int:question_id>/create_answer', views.create_answer),
    path('<int:quiz_id>/edit_quiz', views.edit_quiz),
    path('<int:quiz_id>/delete_quiz', views.delete_quiz),
    path('<int:quiz_id>/update_quiz', views.update_quiz),
    path('<int:quiz_id>/delete_question/<int:question_id>', views.delete_question),
    path('<int:quiz_id>/edit_question/<int:question_id>', views.edit_question),
    path('<int:quiz_id>/edit_question/<int:question_id>/update_question', views.update_question),
    path('<int:quiz_id>/edit_question/<int:question_id>/delete_answer/<int:answer_id>', views.delete_answer),
    path('<int:quiz_id>/edit_question/create_answer/<int:question_id>', views.create_answer),
]