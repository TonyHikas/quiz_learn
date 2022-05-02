from django.contrib import admin

from quiz.models import Question, Answer, Category


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'category')
    ordering = ('id', 'category')
    inlines = [
        AnswerInline
    ]


@admin.register(Answer)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'right')
    ordering = ('id', 'text')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass