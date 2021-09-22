from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse

from users.models import User
from .models import Quiz, Question, Answer, Result


def index(request):
    return render(request, 'quizzes/quiz_index.html')

@login_required
def dashboard(request):     
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
    return redirect('/quizzes/dashboard')
    
def randomizer(request):
    context = {
        "blogs": Blog.objects.order_by('?')[0],
    }
    return render(request, 'randomizer.html', context)

def retake_quiz_info(request, quiz_id, result_id):
    user = request.user
    context = {
        'this_user': User.objects.get(id=user.id),
        'this_quiz': Quiz.objects.get(id=quiz_id),
        'this_result': Result.objects.get(id=result_id)
    }
    return render(request, 'quizzes/retake_quiz.html', context)

def new_score(request, quiz_id, result_id):
    if request.method != "POST":
        return redirect('/quizzes/dashboard')
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
        return redirect(f'/quizzes/{quiz_id}/{result_id}/new_result')

def new_result(request, quiz_id, result_id):
    return render(request, 'quizzes/new_result.html')

def overwrite_result(request, quiz_id, result_id):
    result = Result.objects.get(id=result_id)
    result.percent_score = request.POST['percent_score']
    result.correct_answers = request.POST['correct_answers']
    result.wrong_answers = request.POST['wrong_answers']
    result.total_questions = request.POST['total_questions']
    result.save()
    del request.session['score']
    del request.session['total_questions']
    del request.session['percent_score']
    del request.session['wrong_answers']
    return redirect('/quizzes/dashboard')

def new_quiz(request):
    return render(request, 'quizzes/new_quiz.html')

def create_quiz(request):
    user = User.objects.get(id=request.user.id)
    n = Quiz.objects.create(
        title = request.POST['title'],
        description = request.POST['description'],
        created_by = user
    )
    n.save()
    quiz_id = n.id
    return redirect(f'/quizzes/{quiz_id}/new_question')

def new_question(request, quiz_id):
    return render(request, 'quizzes/new_question.html')

def create_question(request, quiz_id):
    user = User.objects.get(id=request.user.id)
    quiz = Quiz.objects.get(id=quiz_id)
    q = Question.objects.create(
        prompt = request.POST['prompt'],
        created_by = user,
        quiz = quiz
    )
    q.save()
    question_id = q.id
    return redirect(f'/quizzes/{quiz_id}/{question_id}/new_answer')

def new_answer(request, quiz_id, question_id):
    context = {
        'this_quiz': Quiz.objects.get(id=quiz_id),
        'this_question': Question.objects.get(id=question_id)
    }
    return render(request, 'quizzes/new_answer.html', context)

def create_answer(request, quiz_id, question_id):
    this_question = Question.objects.get(id=question_id)
    a = Answer.objects.create(
        text = request.POST['text'],
        correct = request.POST['correct'],
        question = this_question
    )
    a.save()
    total_answers = 0
    for answer in this_question.has_answers.all():
        total_answers += 1

    if total_answers < 2:
        return redirect(f'/quizzes/{quiz_id}/{question_id}/new_answer')
    else:
        return redirect('/quizzes/dashboard')

def edit_quiz(request, quiz_id):
    context = {
        'this_quiz': Quiz.objects.get(id=quiz_id)
    }
    return render(request, 'quizzes/edit_quiz.html', context)

def delete_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    quiz.delete()
    return redirect('/quizzes/dashboard')

def update_quiz(request, quiz_id):
    # validator?
    quiz = Quiz.objects.get(id=quiz_id)
    quiz.title = request.POST['title']
    quiz.description = request.POST['description']
    quiz.save()
    return redirect('/quizzes/dashboard')

def edit_question(request, quiz_id, question_id):
    context = {
        'this_question': Question.objects.get(id=question_id)
    }
    return render(request, 'quizzes/edit_question.html', context)

def delete_question(request, quiz_id, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect(f'/quizzes/{quiz_id}/edit_quiz')

def update_question(request, quiz_id, question_id):
    question = Question.objects.get(id=question_id)
    question.prompt = request.POST['prompt']
    question.save()
    return redirect(f'/quizzes/{quiz_id}/edit_question/{question_id}')

def delete_answer(request, quiz_id, question_id, answer_id):
    answer = Answer.objects.get(id=answer_id)
    answer.delete()
    return redirect(f'/quizzes/{quiz_id}/edit_question/{question_id}')