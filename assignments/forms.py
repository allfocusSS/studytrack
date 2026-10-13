from django import forms

from .models import Assignment


class AssignmentForm(forms.ModelForm):
    deadline = forms.DateField(
        required=False,
        label="Deadline (optional)",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        help_text="Choose a calendar date, or leave blank for no deadline.",
    )

    class Meta:
        model = Assignment
        fields = ["title", "subject", "description", "deadline"]
        labels = {"description": "Description (optional)"}
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}
