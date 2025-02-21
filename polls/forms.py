from django import forms
from .models import Question, User, Learner, Course


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

class LearnerSignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text="")
    password = forms.CharField(widget=forms.PasswordInput)
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    
    class Meta:
        model = User
        fields = ["username", "password"]
        
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            learner = Learner.objects.create(user=user)
            learner.courses.set(self.cleaned_data["courses"])
        return user