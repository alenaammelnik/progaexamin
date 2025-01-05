import matplotlib
matplotlib.use('Agg')  # Добавлено!
import matplotlib.pyplot as plt
import io
import base64
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from polls.models import Question, Choice

matplotlib.use('Agg') 

class QuestionAnalyticsViewSet(viewsets.ViewSet):
    # Получить общую статистику по вопросам
    def list(self, request):
        questions = Question.objects.all()
        data = []
        for question in questions:
            choices = question.choice_set.all()
            total_votes = sum(choice.votes for choice in choices)
            choice_data = [
                {'choice_text': choice.choice_text, 'votes': choice.votes}
                for choice in choices
            ]
            data.append({
                'question': question.question_text,
                'total_votes': total_votes,
                'choices': choice_data
            })
        return Response(data)

    # Получить статистику по конкретному вопросу
    def retrieve(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        choices = question.choice_set.all()

        # Данные для графика
        labels = [choice.choice_text for choice in choices]
        votes = [choice.votes for choice in choices]

        # Создаём диаграмму
        fig, ax = plt.subplots()
        ax.bar(labels, votes, color='blue')
        ax.set_title(f"Статистика для вопроса: {question.question_text}")
        ax.set_ylabel('Голоса')

        # Конвертируем график в base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

        # Сбор данных для ответа
        data = {
            'question': question.question_text,
            'total_votes': sum(votes),
            'choices': [
                {'choice_text': choice.choice_text, 'votes': choice.votes}
                for choice in choices
            ],
            'chart': image_base64
        }
        return Response(data)