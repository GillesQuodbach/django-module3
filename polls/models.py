import datetime
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib import admin
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_choices(self):
        choices = self.choice_set.all()
        total_votes = sum(choice.votes for choice in choices)
        return [
            (choice.choice_text, choice.votes, (choice.votes / total_votes * 100) if total_votes > 0 else 0)
            for choice in choices
        ]

    def get_total_votes(self):
        # nbr total de votes pour cette question
        return self.choice_set.aggregate(Sum("votes"))["votes__sum"] or 0
    # cls représente la classe elle-même ici Question
    # pas besoin d'instance (de créer un object) avec une méthode de classe
    # elle s'applique a toute la classe
    @classmethod
    def get_most_popular_question(cls):
        return max(cls.objects.all(), key=lambda q: q.get_total_votes(), default=None)

    @classmethod
    def get_least_popular_question(cls):
        return min(cls.objects.all(), key=lambda q: q.get_total_votes(), default=None)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


