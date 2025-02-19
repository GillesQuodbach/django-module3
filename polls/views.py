from tempfile import template

from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from .forms import QuestionForm
from .models import Question, Choice
# Create your views here.


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # retourne les 5 dernières questions
        return Question.objects.order_by("-pub_date")[:5]


class AllPollsView(generic.ListView):
    template_name = "polls/all_polls.html"
    context_object_name = "all_questions_list"

    def get_queryset(self):
        # retourne  toutes les questions
        return Question.objects.all()


class StatisticsView(generic.ListView):
    template_name = "polls/statistics.html"
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.all()

    def get_context_data(self, **kwargs):
        # on ajoute des données au context pour les afficher
        context = super().get_context_data(**kwargs)
        # nbr total de question
        context["questions_count"] = Question.objects.count()
        # nbr total de réponses
        context["choices_count"] = Choice.objects.count()
        # nbr total de votes par question
        context["total_votes"] = Choice.objects.aggregate(Sum("votes"))["votes__sum"] or 0
        # moyenne de vote par question
        context["average_votes"] = (
            context["total_votes"] / context["questions_count"] if context["questions_count"] > 0 else 0
        )
        # dernière question enregistrée
        context["latest_question"] = Question.objects.order_by("-pub_date").first()
        #question la plus populaire
        context["most_popular_question"] = Question.get_most_popular_question()
        #question la moins populaire
        context["least_popular_question"] = Question.get_least_popular_question()
        return context


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class AddQuestionView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "polls/add_question.html"
    success_url = reverse_lazy("polls:index")

    def form_valid(self, form):
        # sauvegarde de la question
        self.object = form.save()

        # on récupère les choix
        choices = [
            form.cleaned_data.get("choice1"),
            form.cleaned_data.get("choice2"),
            form.cleaned_data.get("choice3"),
            form.cleaned_data.get("choice4"),
            form.cleaned_data.get("choice5"),
        ]

        # on crée les choix non vides
        for choice_text in choices:
            if choice_text:
                Choice.objects.create(question=self.object, choice_text=choice_text)
        return redirect(self.success_url)



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def frequency(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.get_choices()
    return render(request, "polls/frequency.html", {"question": question, "choices": choices})
