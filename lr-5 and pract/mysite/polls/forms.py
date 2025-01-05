from django import forms
from .models import Question, Choice


class QuestionForm(forms.ModelForm):
    choices = forms.CharField(widget=forms.Textarea, help_text="Введите варианты ответа по одному в строке.")

    class Meta:
        model = Question
        fields = ['question_text']

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()
            choices = self.cleaned_data['choices'].splitlines()
            for choice_text in choices:
                if choice_text.strip():  # Создаем варианты, если текст не пустой
                    Choice.objects.create(question=question, choice_text=choice_text)
        return question