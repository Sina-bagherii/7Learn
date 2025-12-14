from django import forms


class QuestionForm(forms.Form):
    question = forms.CharField(
        label="Ask anything",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Describe your question for ChatGPT...",
            }
        ),
    )
