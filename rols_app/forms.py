from django import forms
from .models import Device, Ticket, TicketComment

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['serial_number', 'device_type', 'model', 'assigned_to', 'date_assigned', 'notes']
        widgets = {
            'date_assigned': forms.DateInput(attrs={'type': 'date'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'device', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'أضف تعليقك هنا...'}),
        }

class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'assigned_to', 'resolution']
        widgets = {
            'resolution': forms.Textarea(attrs={'rows': 3}),
        }