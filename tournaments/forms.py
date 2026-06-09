from django import forms
from tournaments.models import Torneio

class TorneioForm(forms.ModelForm):

    cidade = forms.CharField(
        widget = forms.TextInput(
            attrs={

            }
        )
    )

    estado = forms.CharField(
        widget = forms.TextInput(
            attrs={
                
            }
        )
    )

    numero = forms.CharField(
        widget = forms.TextInput(
            attrs={
                
            }
        )
    )

    bairro = forms.CharField(
        widget = forms.TextInput(
            attrs={
                
            }
        )
    )

    lagradouro = forms.CharField(
        widget = forms.TextInput(
            attrs={
                
            }
        )
    )

    complemento = forms.CharField(
        widget = forms.TextInput(
            attrs={
                
            }
        )
    )

    class Meta:

        model = Torneio

        fields = [
            'nome',
            'descricao',
            'numero_maximo_participantes',
            'valor_inscricao',
            'premiacoes',
            'tipo',
            'formato_torneio',
            'formato_jogo',
            'numero_rodadas',
            'data_inicio'
        ]

        widgets = {

            'nome': forms.TextInput(
                attrs={

                }
            ),

            'descricao': forms.Textarea(
                attrs={
                }
            ),

            'numero_maximo_participantes': forms.NumberInput(
                attrs={
                }
            ),

            'valor_inscricao': forms.NumberInput(
                attrs={

                }
            ),

            'cidade': forms.TextInput(
                attrs={
                }
            ),

            'premiacoes': forms.Textarea(
                attrs={
                }
            ),

            'tipo': forms.Select(
                attrs={
                }
            ),

            'formato_torneio': forms.Select(
                attrs={
                }
            ),


            'formato_jogo': forms.Select(
                attrs={
                }
            ),

            'numero_rodadas': forms.NumberInput(
                attrs={
                }
            ),

            'data_inicio': forms.DateTimeInput(
                attrs={
                }
            )
        }