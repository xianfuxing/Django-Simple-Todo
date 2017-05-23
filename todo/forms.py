from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
	PRIORITY_CHOICES = (
		('1', "important"),
		('2', "warning"),
		('3', "info"),
	)

	priority = forms.ChoiceField(widget=forms.RadioSelect(), choices=PRIORITY_CHOICES)
	def __init__(self, *args, **kwargs):
		super(TodoForm, self).__init__(*args, **kwargs)
		self.fields['todo'].help_text = '添加Todo'

	
	class Meta:
		model = Todo
		fields = ['todo', 'priority']
		widgets = {'todo': forms.Textarea(attrs={'rows': 0,
                                                 'cols': 0,
                                                 'class': 'txtodo',
                                                 'id': 'txtodo',
                                                 'resize':'none'}),
		}