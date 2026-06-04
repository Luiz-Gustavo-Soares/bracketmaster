from django.shortcuts import render, get_object_or_404, redirect




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
            'status': 'created' 
        },
        {
            'titulo': 'Mix Diamantina Dia D de Dado',
            'descricao': 'Boas-vindas ao melhor campeonato de Commander do mundo, e até de Diamantina!',
            'formato': 'Commander',
            'data': '14/06/26',
            'imagem_capa': 'media/capas_campeonato/lobinho_magic.png',
            'autor_nome': 'Nissa Revane',
            'autor_avatar': 'media/avatares/nissa.png',
            'status': 'open' 
        },
        {
            'titulo': 'Maior Campeonato de Todos os Tempos',
            'descricao': 'Aqui decidiremos o próximo CEO da Wizards of the Coast, porque o trem tá feio.',
            'formato': 'Modern',
            'data': '21/06/26',
            'imagem_capa': 'media/capas_campeonato/cidade_vermelha.png',
            'autor_nome': 'Gideon Jura',
            'autor_avatar': 'media/avatares/gideon.png',
            'status': 'running' 
        },
        {
            'titulo': 'Só Dinos e Mais Nada, Uhum!',
            'descricao': 'Tá no nome. Se vier encher o saco te lapo a mordida, ou o meu amigo Joãozinho comedor de ovo!',
            'formato': 'Commander',
            'data': '01/07/26',
            'imagem_capa': 'media/capas_campeonato/dinos_magic.png',
            'autor_nome': 'Gishath, Avatar do Sol',
            'autor_avatar': 'media/avatares/gisha.png',
            'status': 'closed' 
        },
        {
            'titulo': 'Redraft Gótico de Innistrad Muito Goth',
            'descricao': 'Venha de preto.',
            'formato': 'Draft',
            'data': '14/08/26',
            'imagem_capa': 'media/capas_campeonato/pretos.png',
            'autor_nome': 'Liliana Vess',
            'autor_avatar': 'media/avatares/lilia.png',
            'status': 'finished' 
        }
    ]

    context = {
        'torneios_destacados': torneios_mock
    }
    user = request.user
    return render(request, 'index.html', context)

from django.shortcuts import render
from datetime import date

# --- CLASSES MOCK PARA SIMULAR O BANCO DE DADOS ---
class MockDeck:
    def __init__(self, nome):
        self.nome = nome

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
        self.profile_imagem = None  # O seu fallback do Atraxa/Nissa vai assumir aqui
        self.banner = None          # O seu fallback do banner vai assumir aqui

    # Simula o ".all()" do Django ORM que você usou no HTML
    class DecksFavoritos:
        def all(self):
            return [MockDeck("Mono-Green Ramp"), MockDeck("Zendikar Elementals")]
    
    decks_favoritos = DecksFavoritos()

# --- A FUNÇÃO DA VIEW ---
def profile_view(request, nickname):
    """Renderiza o perfil público de um jogador específico."""
    
    # Se a busca for pela Nissa, mandamos os dados completos
    if nickname.lower() == 'nissarevane':
        context = {
            'profile': MockProfile(),
            'taxa_vitoria': 74.5,
            'variacao_winrate': 2.1,
            'historico': [
                MockHistorico(
                    MockTorneio("Zendikar Rising Championship", "Standard", 128, date(2026, 5, 15)), 
                    "Mono-Green Aggro", 1, 500
                ),
                MockHistorico(
                    MockTorneio("Liga Local de Kaladesh", "Pioneer", 64, date(2026, 4, 10)), 
                    "Golgari Midrange", 4, 250
                ),
                MockHistorico(
                    MockTorneio("Torneio Casual da Taverna", "Commander", 4, date(2026, 3, 22)), 
                    None, 2, 100
                )
            ]
        }
    else:
        # Se clicar no Gideon ou qualquer outro que ainda não mockamos
        class GenericoProfile:
            nickname = nickname
            user = type('User', (), {'username': nickname, 'pk': 2})()
            location = "Desconhecido"
            bio = "Jogador misterioso..."
            profile_imagem = None
            banner = None
            decks_favoritos = type('Decks', (), {'all': lambda: []})()
            
        context = {
            'profile': GenericoProfile(),
            'taxa_vitoria': 50.0,
            'historico': []
        }

    return render(request, 'profile_view.html', context)

# ... (suas outras funções home e dashboard estão aqui em cima) ...

# 1. COLE AS CLASSES MOCK AQUI (Elas simulam as tabelas do Banco de Dados)
class MockDeck:
    def __init__(self, nome):
        self.nome = nome

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
        self.bio = "Planeswalker focada em magia verde, animando terrenos e invocando elementais poderosos."
        self.profile_imagem = None 
        self.banner = None         

    class DecksFavoritos:
        def all(self):
            return [MockDeck("Mono-Green Ramp"), MockDeck("Zendikar Elementals")]
    
    decks_favoritos = DecksFavoritos()

# 2. COLE A FUNÇÃO DA TELA LOGO ABAIXO DAS CLASSES
def profile_view(request, nickname):
    if nickname.lower() == 'nissarevane':
        context = {
            'profile': MockProfile(),
            'taxa_vitoria': 74.5,
            'variacao_winrate': 2.1,
            'historico': [
                MockHistorico(MockTorneio("Zendikar Rising", "Standard", 128, date(2026, 5, 15)), "Mono-Green", 1, 500),
                MockHistorico(MockTorneio("Liga Kaladesh", "Pioneer", 64, date(2026, 4, 10)), "Golgari", 4, 250),
            ]
        }
    else:
        # Perfil genérico se não for a Nissa
        class GenericoProfile:
            nickname = nickname
            user = type('User', (), {'username': nickname, 'pk': 2})()
            location = "Desconhecido"
            bio = "Jogador misterioso..."
            profile_imagem = None
            banner = None
            decks_favoritos = type('Decks', (), {'all': lambda: []})()
            
        context = {
            'profile': GenericoProfile(),
            'taxa_vitoria': 50.0,
            'historico': []
        }

    return render(request, 'users/profile_view.html', context)