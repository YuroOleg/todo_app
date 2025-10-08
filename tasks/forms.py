from django import forms 
from .models import Task
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
import pytz

class TaskForm(forms.ModelForm):
    """Form for creating and updating tasks"""
    deadline_date = forms.DateField(
        widget = forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',   
            }
        ),
        input_formats=['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%Y/%m/%d']
    )
    
    deadline_time = forms.TimeField(widget = forms.TimeInput(attrs={
                'type': 'time',   
            }))

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'reminder']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_classes + ' form-control').strip()

            if field_name == "description":
                existing_styles = field.widget.attrs.get('style', '')
                field.widget.attrs['style'] = (existing_styles + ' resize: none;').strip()


    def clean(self):
        """Local time convertion to UTC"""
        cleaned = super().clean()

        deadline_date = cleaned.get('deadline_date')
        deadline_time = cleaned.get('deadline_time')

        if deadline_date and deadline_time: 
            deadline_datetime = datetime.combine(deadline_date, deadline_time)

            local_timezone = pytz.timezone(self.user.timezone)
            local_datetime = local_timezone.localize(deadline_datetime)
            utc_datetime = local_datetime.astimezone(pytz.UTC)


            if utc_datetime < timezone.now():
                self.add_error('deadline_date', ValidationError("Deadline time has already passed"))

            cleaned['utc_datetime'] = utc_datetime
            cleaned['local_datetime'] = deadline_datetime

        return cleaned
    

    def save(self, commit=True):
        task = super().save(commit=False)
        task.deadline = self.cleaned_data.get('utc_datetime')
        task.local_deadline = self.cleaned_data.get('local_datetime')
        task.user = self.user
        if commit: 
            task.save()

        return task

        
        

