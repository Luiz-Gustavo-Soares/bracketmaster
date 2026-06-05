from django.shortcuts import render
from datetime import date

# 1. Importamos a sua classe MockTorneio que já existe no index.py
from .index import MockTorneio 

def torneios_view(request):
    
    # 2. Criamos uma base de torneios (usando os mesmos dados do seu print)
    torneio_1 = MockTorneio("Mix Diamantina Dia D de Dado", "Commander", 128, date(2026, 6, 14))
    torneio_2 = MockTorneio("Maior Campeonato de Todos os Tempos", "Modern", 64, date(2026, 6, 21))
    torneio_3 = MockTorneio("Só Dinos e Mais Nada, Uhum!", "Commander", 32, date(2026, 7, 1))
    torneio_4 = MockTorneio("Redraft Gótico de Innistrad", "Draft", 16, date(2026, 6, 14))

    # 3. Multiplicamos por 2 para termos 8 torneios exatos na tela
    lista_torneios = [torneio_1, torneio_2, torneio_3, torneio_4] * 2

    # 4. Enviamos os dados para o HTML no 'context'
    context = {
        'torneios': lista_torneios,
        'total_torneios': len(lista_torneios) # Vai enviar o número 8 dinamicamente
    }

    return render(request, 'torneios.html', context)