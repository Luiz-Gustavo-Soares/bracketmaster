from django import forms
from tournaments.models import Torneio

class TorneioForm(forms.ModelForm):

    cidade = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class":"form-control", "placeholder":"Cidade"
            }
        )
    )

    estado = forms.CharField(
        max_length=2,
        widget = forms.TextInput(
            attrs={
                "class":"form-control", "placeholder":"Estado (sigla)"
            }
        )
    )

    numero = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class":"form-control", "placeholder":"Número"
            }
        )
    )

    bairro = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class":"form-control", "placeholder":"Bairro"
            }
        )
    )

    lagradouro = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class":"form-control", "placeholder":"Logradouro"
                
            }
        )
    )

    complemento = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class":"form-control", "placeholder":"Complemento"
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
                    "class":"form-control", 
                    "placeholder":"O nome do torneio"
                }
            ),

            'descricao': forms.Textarea(
                attrs={
                    "class":"form-control" , "rows":"3", "placeholder":"Sobre o torneio"
                }
            ),

            'numero_maximo_participantes': forms.NumberInput(
                attrs={
                    "class":"form-control", "placeholder":"Quantidade de participantes"
                }
            ),

            'valor_inscricao': forms.NumberInput(
                attrs={
                    "class":"form-control" , "placeholder":"Valor da inscrição em R$"

                }
            ),

            'premiacoes': forms.Textarea(
                attrs={
                    "class":"form-control",  "rows":"2", "placeholder":"Informe a premiação de cada colocação, uma por linha, começando pelo 1º lugar"
                }
            ),

            'tipo': forms.Select(
                attrs={
                    "class":"form-control"
                }
            ),

            'formato_torneio': forms.Select(
                attrs={
                    "class":"form-control" 
                }
            ),


            'formato_jogo': forms.Select(
                attrs={
                    "class":"form-control" 
                }
            ),

            'numero_rodadas': forms.NumberInput(
                attrs={
                    "class":"form-control", "placeholder":"Duração do torneio em rodadas"
                }
            ),

            'data_inicio': forms.DateTimeInput(
                attrs={
                    'type':'datetime-local',
                    "class":"form-control"
                }
            )
        }