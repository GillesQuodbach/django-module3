from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    # champ faisant partie du model Choice donc doivent
    # être créé à la main
    choice1 = forms.CharField(label="Choix 1", required=False)
    choice2 = forms.CharField(label="Choix 2", required=False)
    choice3 = forms.CharField(label="Choix 3", required=False)
    choice4 = forms.CharField(label="Choix 4", required=False)
    choice5 = forms.CharField(label="Choix 5", required=False)

    # champs du model Question donc généré automatiquement
    class Meta:
        model = Question
        fields = ["question_text"]

