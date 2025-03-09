from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=300)
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name='questions',unique = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='answers')
    text = models.CharField(max_length=60)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

