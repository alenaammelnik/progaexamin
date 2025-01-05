from django.db import models
from polls.models import Question, Choice


class VoteAnalytics(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    total_votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analytics for: {self.question.question_text}"