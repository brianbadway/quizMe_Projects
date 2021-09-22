from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse

from users.models import User
from .models import Quiz, Question, Answer, Result

def index(request):
    return render(request, 'registration/login.html')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/users/register')       
    context = {
        'all_quizzes': Quiz.objects.all(),
    }
    return render(request, 'quizzes/dashboard.html', context)

@login_required
def quiz_info(request, quiz_id):
    user = request.user
    context = {
        'this_user': User.objects.get(id=user.id),
        'this_quiz': Quiz.objects.get(id=quiz_id)
    }
    return render(request, 'quizzes/Quiz_info.html', context)

def create_score(request, quiz_id):
    if request.method != "POST":
        return redirect('/')
    # Insert answer validator
    # redirect if errors
    else:
        if request.user.id:
            this_quiz = Quiz.objects.get(id=quiz_id)
            total_questions = 0
            score = 0
            for question in this_quiz.has_questions.all():
                total_questions+= 1
                print(question.id)
                print(request.POST['question_'+str(question.id)+'_'+(question.prompt)])
                if request.POST['question_'+str(question.id)+'_'+(question.prompt)] == 'True':
                    score += 1
                else:
                    score += 0
            percent_score = (score*100)/total_questions
            percent_score = int(percent_score)
            wrong_answers = total_questions - score
            request.session['score'] = score
            request.session['total_questions'] = total_questions
            request.session['percent_score'] = percent_score
            request.session['wrong_answers'] = wrong_answers
            print(request.POST)
            print(score)
            print(total_questions)
            print(request.session['score'])
        return redirect(f'/quizzes/{quiz_id}/result')

def result(request, quiz_id):
    return render(request, 'quizzes/Quiz_Result.html')

def save_result(request, quiz_id):
    user = User.objects.get(id=request.user.id)
    quiz = Quiz.objects.get(id=quiz_id)
    # if user.has_results.quiz.id == quiz_id:
    #     # if score is higher
    #     overwrite_result = Result.objects.get(id=)
    # else:
    Result.objects.create(
        percent_score = request.POST['percent_score'],
        correct_answers = request.POST['correct_answers'],
        wrong_answers = request.POST['wrong_answers'],
        total_questions = request.POST['total_questions'],
        quiz = quiz,
        user = user
    )
    del request.session['score']
    del request.session['total_questions']
    del request.session['percent_score']
    del request.session['wrong_answers']
    return redirect('/')
    
def randomizer(request):
    context = {
        "blogs": Blog.objects.order_by('?')[0],
    }
    return render(request, 'randomizer.html', context)
