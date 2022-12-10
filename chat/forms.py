from django import forms
from django.contrib.auth.models import User
from chat.models import MessageModel


class ChatForm(forms.Form):
    username=forms.CharField(label='',help_text='Who do you wanna talk to?')

class MessageForm(forms.ModelForm):
    body=forms.CharField(label='',max_length=1000,required=False,widget=forms.TextInput(attrs={
        'placeholder':'Say something...',
        'class':'fw-bold'
    }))
    image=forms.ImageField(required=False)

    class Meta:
        model=MessageModel
        fields=['body','image']



