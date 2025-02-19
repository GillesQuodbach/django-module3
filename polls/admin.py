from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["question_text", "pub_date"]
    ordering = ["pub_date"]
    search_fields = ["question_text", "pub_date"]
    # en changeant l'ordre on modifie l'affichage dans l'admin
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "votes", "question_id"]
    list_filter = ["choice_text", "votes", "question_id"]
    ordering = ["question_id"]
    search_fields = ["choice_text"]


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)




