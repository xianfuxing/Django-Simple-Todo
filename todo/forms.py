from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
	PRIORITY_CHOICES = (
		('1', "important"),
		('2', "warning"),
		('3', "general"),
	)

	priority = forms.ChoiceField(widget=forms.RadioSelect(), choices=PRIORITY_CHOICES)
	
	class Meta:
		model = Todo
		fields = ['todo', 'priority']