from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Category Name'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=300, verbose_name=_('Question Text'))
    category = models.OneToOneField(
        'Category', on_delete=models.CASCADE, related_name='questions', unique=True, verbose_name=_('Category')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers', verbose_name=_('Question')
    )
    text = models.CharField(max_length=60, verbose_name=_('Answer Text'))
    is_correct = models.BooleanField(default=False, verbose_name=_('Is Correct'))

    def __str__(self):
        return self.text


