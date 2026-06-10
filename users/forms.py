from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "LordCalabreso"
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "placeholder": "lord.calabreso@bracketmaster.gg",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "••••••••"
            }
        )
    )


class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "placeholder": "calabresinho@bracketmaster.gg",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "••••••••"
            }
        )
    )


class ProfileForm(forms.ModelForm):

    cidade = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'class':"form-control",
                'placeholder':"Sua cidade"
            }
        )
    )

    estado = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'class':"form-control",
                'placeholder':"Sigla do estado (ex: SP)"
            }
        )
    )

    class Meta:
        model = Profile
        fields = ['nickname', 'bio'] #, 'avatar']
        widgets = {
            'nickname': forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':"Seu apelido na plataforma"
                }
            ),

            'bio': forms.Textarea(
                attrs={
                    'class':"form-control",
                    'rows':"4",
                    'placeholder':"Fale um pouco sobre você e seu estilo de jogo..."
                }
            ),

            # 'avatar': forms.Select(
            #     attrs={
                    
            #     }
            # )
        }
