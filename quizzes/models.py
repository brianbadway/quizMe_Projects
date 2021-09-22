from django.db import models
from users.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name="quizzes_created", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Question(models.Model):
    prompt = models.CharField(max_length=255,null=True)
    created_by = models.ForeignKey(User, related_name="questions_created", on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name="has_questions", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Answer(models.Model):
    text = models.CharField(max_length=255, null=True)
    correct = models.BooleanField(default=False)
    # created_by = models.ForeignKey(User, related_name="questions_created", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="has_answers", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Result(models.Model):
    percent_score = models.IntegerField()
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    total_questions = models.IntegerField()
    quiz = models.ForeignKey(Quiz, related_name="results_saved", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="has_results", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)