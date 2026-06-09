from django.shortcuts import render
from datetime import date
from django.core.paginator import Paginator # 1. IMPORTANTE: Importamos o paginador nativo do Django
from .index import MockTorneio 

def explore_torneios(request):
    
    # 2. Base de torneios simulados
    torneio_1 = MockTorneio("Mix Diamantina Dia D de Dado", "Commander", 128, date(2026, 6, 14))
    torneio_2 = MockTorneio("Maior Campeonato de Todos os Tempos", "Modern", 64, date(2026, 6, 21))
    torneio_3 = MockTorneio("Só Dinos e Mais Nada, Uhum!", "Commander", 32, date(2026, 7, 1))
    torneio_4 = MockTorneio("Redraft Gótico de Innistrad", "Draft", 16, date(2026, 6, 14))

    lista_torneios = [torneio_1, torneio_2, torneio_3, torneio_4] * 2

    # 3. Configura o Paginator para quebrar a lista de 4 em 4 itens por página
    paginator = Paginator(lista_torneios, 4)

    # 4. Captura o número da página atual que o usuário clicou 
    page_number = request.GET.get('page')

    # 5. Gera o objeto final da página atual contendo apenas os 4 torneios da vez
    torneios_paginados = paginator.get_page(page_number)

    # 6. Enviamos os dados para o HTML no 'context'
    context = {
        'torneios': torneios_paginados,       # O HTML vai receber o objeto paginado e ler os loops normalmente
        'total_torneios': len(lista_torneios)  # Mantém o número total de registros (8) fixo no cabeçalho
    }
    
    return render(request, 'explore_torneios.html', context)