from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
	PRIORITY_CHOICES = (
		('0', "important"),
		('1', "warning"),
		('2', "general"),
	)

	priority = forms.ChoiceField(widget=forms.RadioSelect(), choices=PRIORITY_CHOICES)
	
	class Meta:
		model = Todo
		fields = ['todo', 'priority']