from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=300)
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name='questions')
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='answers')
    text = models.CharField(max_length=60)
class Category(models.Model):
    name = models.CharField(max_length=100)

