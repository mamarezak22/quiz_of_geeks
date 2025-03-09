from django.contrib import admin

from questions.models import Question, Answer, Category


# Register your models here.
class AnswerInlineAdmin(admin.TabularInline):
    model = Answer
    extra = 1
class QuestionAdmin(admin.ModelAdmin):
    class Meta:
        model = Question
        inlines = [AnswerInlineAdmin]
        filter_horizontal = ('category',)
class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category
