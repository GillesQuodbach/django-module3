from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("all/", views.AllPollsView.as_view(), name="all_polls"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/frequency", views.frequency, name="frequency"),
    path("statistics/", views.StatisticsView.as_view(), name="statistics"),
    path("add/", views.AddQuestionView.as_view(), name="add_question"),
]
