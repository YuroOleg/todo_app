from django import forms
from .models import Task
from django.utils import timezone
from datetime import datetime

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority']

    deadlineDate = forms.DateField(
        label="Deadline Date", 
        input_formats=[
            "%Y-%m-%d",          
            "%d.%m.%Y",
            "%d/%m/%Y",       
        ],
        required=True,
        )
    deadlineTime = forms.TimeField(label="Deadline Time", required=True)

    def clean(self):
        cleaned = super().clean()

        date = cleaned.get('deadlineDate')
        time = cleaned.get('deadlineTime')
        
        if date and time:
            if  datetime.combine(date, time) < datetime.now():
                self.add_error("deadlineDate", "This time and date have already passed")

        return cleaned
    
    def save(self, commit=True):
        task = super().save(commit=False)

        date = self.cleaned_data['deadlineDate']
        time = self.cleaned_data['deadlineTime']

        task.deadline = timezone.make_aware(datetime.combine(date, time))

        if commit:
            task.save()

        return task
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.deadline:
            self.fields['deadlineDate'].initial = self.instance.deadline.date()
            self.fields['deadlineTime'].initial = self.instance.deadline.time()

        for field_name in ['title', 'description', 'priority']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'style': 'resize: none;'})

        self.fields['deadlineDate'].widget.attrs.update({'class': 'form-control'})
        self.fields['deadlineTime'].widget.attrs.update({'class': 'form-control'})



        

        