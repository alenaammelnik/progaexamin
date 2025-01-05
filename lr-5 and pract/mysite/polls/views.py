from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Question, Choice
from .forms import QuestionForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms_auth import RegisterForm
import requests
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils.dateparse import parse_date

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# Обработка голосования
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Получаем выбранный ответ
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Если выбор не сделан — показать страницу вопроса с ошибкой
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Вы не выбрали ответ.",
        })
    else:
        # Увеличиваем количество голосов
        selected_choice.votes += 1
        selected_choice.save()
        # Перенаправляем пользователя на страницу результатов
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:index')  # После сохранения перенаправляем на главную страницу
    else:
        form = QuestionForm()
    return render(request, 'polls/create_question.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:index')
    else:
        form = RegisterForm()
    return render(request, 'polls/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('polls:index')
    else:
        form = AuthenticationForm()
    return render(request, 'polls/login.html', {'form': form})

def analytics_view(request, question_id):
    response = requests.get(f"http://127.0.0.1:8000/analytics/analytics/{question_id}/")
    data = response.json()
    return render(request, 'polls/analytics.html', data)

def search(request):
    return render(request, 'polls/search.html')


def filter_polls(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Преобразуем строки в даты
    if start_date:
        start_date = parse_date(start_date)
    if end_date:
        end_date = parse_date(end_date)

    # Фильтруем голосования по датам
    polls = Question.objects.all()
    if start_date:
        polls = polls.filter(pub_date__gte=start_date)
    if end_date:
        polls = polls.filter(pub_date__lte=end_date)

    # Возвращаем данные в формате JSON
    data = [{'id': poll.id, 'question': poll.question_text} for poll in polls]
    return JsonResponse(data, safe=False)