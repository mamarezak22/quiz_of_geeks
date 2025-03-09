from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from questions.models import Question, Answer, Category

# Inline for Answer model
class AnswerInlineAdmin(admin.TabularInline):
    model = Answer
    extra = 1
    verbose_name = _('Answer')
    verbose_name_plural = _('Answers')

# Register Question model in admin
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    class Meta:
        model = Question
    inlines = [AnswerInlineAdmin]
    list_display = ('text', 'category', 'created_at')  # Display fields in the list
    search_fields = ['text', 'category__name']  # Search functionality
    fieldsets = (
        (None, {
            'fields': ('text', 'category', 'created_at')
        }),
    )
    verbose_name = _('Question')
    verbose_name_plural = _('Questions')

# Register Category model in admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category
    list_display = ('name',)
    search_fields = ['name']
    verbose_name = _('Category')
    verbose_name_plural = _('Categories')

