from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """게시글 작성/수정 폼"""
    
    class Meta:
        model = Post
        fields = ['image', 'content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '문구를 입력하세요...',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'image': '이미지',
            'content': '내용',
        }

class CommentForm(forms.ModelForm):
    """댓글 작성/수정 폼"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '댓글을 입력하세요...',
            }),
        }
        labels = {
            'content': '',
        }