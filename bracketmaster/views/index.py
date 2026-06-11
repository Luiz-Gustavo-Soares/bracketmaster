from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
from django.core.paginator import Paginator
from django.http import JsonResponse




def home(request):
    """Pagina inicial da aplicação"""

    # Simulando o que virá do Banco de Dados futuramente pra testar essa bomba
    torneios_mock = [
        {
            'titulo': 'A Última Evolução',
            'descricao': 'A perfeição está próxima. Em um mundo à beira do colapso, apenas aqueles capazes de evoluir além dos limites sobreviverão. A última etapa da transformação começou.',
            'formato': 'Commander',
            'data': '29/06/26',
            'imagem_capa': 'media/capas_campeonato/monumento_magic.jpg',
            'autor_nome': 'Atraxa',
            'autor_avatar': 'media/avatares/Atraxa.jpg',
            'status': 'CRIADO' 
        },
        {
            'titulo': 'Mix Diamantina Dia D de Dado',
            'descricao': 'Boas-vindas ao melhor campeonato de Commander do mundo, e até de Diamantina!',
            'formato': 'Commander',
            'data': '14/06/26',
            'imagem_capa': 'media/capas_campeonato/lobinho_magic.jpg',
            'autor_nome': 'Nissa Revane',
            'autor_avatar': 'media/avatares/nissa.jpg',
            'status': 'ABERTA' 
        },
        {
            'titulo': 'Maior Campeonato de Todos os Tempos',
            'descricao': 'Aqui decidiremos o próximo CEO da Wizards of the Coast, porque o trem tá feio.',
            'formato': 'Modern',
            'data': '21/06/26',
            'imagem_capa': 'media/capas_campeonato/cidade_vermelha.jpg',
            'autor_nome': 'Gideon Jura',
            'autor_avatar': 'media/avatares/gideon.jpg',
            'status': 'EM_ANDAMENTO' 
        },
        {
            'titulo': 'Só Dinos e Mais Nada, Uhum!',
            'descricao': 'Tá no nome. Se vier encher o saco te lapo a mordida, ou o meu amigo Joãozinho comedor de ovo!',
            'formato': 'Commander',
            'data': '01/07/26',
            'imagem_capa': 'media/capas_campeonato/dinos_magic.jpg',
            'autor_nome': 'Gishath, Avatar do Sol',
            'autor_avatar': 'media/avatares/gisha.jpg',
            'status': 'FECHADA' 
        },
        {
            'titulo': 'Redraft Gótico de Innistrad Muito Goth',
            'descricao': 'Venha de preto.',
            'formato': 'Draft',
            'data': '14/08/26',
            'imagem_capa': 'media/capas_campeonato/pretos.jpg',
            'autor_nome': 'Liliana Vess',
            'autor_avatar': 'media/avatares/lilia.jpg',
            'status': 'FINALIZADO' 
        }
    ]

    context = {
        'torneios_destacados': torneios_mock
    }
    return render(request, 'index.html', context)

# --- CLASSES MOCK PARA SIMULAR O BANCO DE DADOS ---
class MockDeck:
    def __init__(self, nome):
        self.nome = nome

class MockImage:
    """Simula um ImageField do Django, que possui o atributo .url"""
    def __init__(self, url_caminho):
        self.url = url_caminho

class MockTorneio:
    def __init__(self, nome, formato, total_jogadores, data):
        self.nome = nome
        self.formato = formato
        self.total_jogadores = total_jogadores
        self.data = data

class MockHistorico:
    def __init__(self, torneio, deck, posicao, pontos):
        self.torneio = torneio
        self.deck = deck
        self.posicao = posicao
        self.pontos = pontos

class MockProfile:
    class User:
        pk = 1
        username = "NissaRevane"

    def __init__(self):
        self.nickname = "NissaRevane"
        self.user = self.User()
        self.location = "Zendikar"
        self.bio = "Planeswalker focada em magia verde, animando terrenos e invocando elementais poderosos. Defensora implacável do multiverso."
        self.profile_imagem = None  
        self.banner = None          

    class DecksFavoritos:
        def all(self):
            return [MockDeck("Mono-Green Ramp"), MockDeck("Zendikar Elementals")]
    
    decks_favoritos = DecksFavoritos()

# --- A FUNÇÃO DA VIEW ---
def profile_view(request, nickname):
    """Renderiza o perfil público de um jogador específico."""
    
    if nickname.lower() == 'nissarevane':
        lista_de_torneios = [
            MockHistorico(MockTorneio("Torneio 1", "Standard", 128, date(2026, 5, 15)), "Deck 1", 1, 500),
            MockHistorico(MockTorneio("Torneio 2", "Pioneer", 64, date(2026, 4, 10)), "Deck 2", 4, 250),
            MockHistorico(MockTorneio("Torneio 3", "Commander", 4, date(2026, 3, 22)), None, 2, 100),
        ] * 6
                
        paginator = Paginator(lista_de_torneios, 5) 
        numero_da_pagina = request.GET.get('page')
        page_obj = paginator.get_page(numero_da_pagina)

        context = {
            'profile': MockProfile(),
            'taxa_vitoria': 74.5,
            'variacao_winrate': 2.1,
            'historico': page_obj  
        }    
        
    else:
        class GenericoProfile:
            def __init__(self, nome_buscado):
                self.nickname = nome_buscado
                self.user = type('User', (), {'username': nome_buscado, 'pk': 2})()
                self.location = "Desconhecido"
                self.bio = "Jogador misterioso..."
                self.profile_imagem = None
                self.banner = None
                self.decks_favoritos = type('Decks', (), {'all': lambda: []})()
            
        context = {
            'profile': GenericoProfile(nickname),
            'taxa_vitoria': 50.0,
            'historico': []
        }

    return render(request, 'users/profile_view.html', context)


def toggle_like_view(request, nickname):
    """View para processar o like sem recarregar a página"""
    if request.method == "POST":
        # Aqui você buscaria o perfil real no banco:
        # target_profile = get_object_or_404(Profile, user__username=nickname)
        
        # Como estamos no Mock, vamos apenas simular a resposta de sucesso
        # Quando tiver o banco real, você colocará a lógica de .add() e .remove() aqui
        liked = True 
        
        return JsonResponse({
            'status': 'success',
            'is_liked': liked,
            'msg': 'Like processado com sucesso'
        })
    return JsonResponse({'status': 'error'}, status=400)