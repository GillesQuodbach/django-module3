from django.contrib import admin
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date"]
    list_filter = ["question_text", "pub_date"]
    ordering = ["pub_date"]
    search_fields = ["question_text", "pub_date"]
    # en changeant l'ordre on modifie l'affichage dans l'admin
    fields = ["pub_date","question_text"]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "votes", "question_id"]
    list_filter = ["choice_text", "votes", "question_id"]
    ordering = ["question_id"]
    search_fields = ["choice_text"]


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)




