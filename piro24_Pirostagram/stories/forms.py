from django import forms
from .models import StoryImage


class StoryImageForm(forms.ModelForm):
    """스토리 이미지 폼 - 한 장씩 업로드"""
    
    class Meta:
        model = StoryImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'image': '이미지',
        }