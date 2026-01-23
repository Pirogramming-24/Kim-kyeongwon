from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignUpForm(UserCreationForm):
    """회원가입 폼"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '이메일'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '사용자 이름'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 비밀번호 필드에도 CSS 클래스 추가
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '비밀번호'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '비밀번호 확인'
        })

class LoginForm(AuthenticationForm):
    """로그인 폼"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '사용자 이름'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀번호'
        })
    )

class ProfileUpdateForm(forms.ModelForm):
    """프로필 수정 폼"""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '사용자 이름'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '이메일'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '이름'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '성'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '자기소개',
                'rows': 4
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }