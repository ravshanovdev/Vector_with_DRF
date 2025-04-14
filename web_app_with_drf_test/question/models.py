from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    body = models.TextField()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f"user: {self.user.username}"\
               f"Question: {self.question}"\
               f"body: {self.body}"
