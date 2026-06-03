from django.shortcuts import render, get_object_or_404, redirect



def home(request):
    """Pagina inicial da aplicação"""

    # Simulando o que virá do Banco de Dados futuramente pra testar essa bomba
    torneios_mock = [
        {
            'titulo': 'Mix Diamantina Dia D de Dado',
            'descricao': 'Boas-vindas ao melhor campeonato de Commander do mundo, e até de Diamantina!',
            'formato': 'Commander',
            'data': '14/06/26',
            'imagem_capa': 'media/capas_campeonato/lobinho_magic.png',
            'autor_nome': 'Nissa Revane',
            'autor_avatar': 'media/avatares/nissa.png'
        },
        {
            'titulo': 'Maior Campeonato de Todos os Tempos',
            'descricao': 'Aqui decidiremos o próximo CEO da Wizards of the Coast, porque o trem tá feio.',
            'formato': 'Modern',
            'data': '21/06/26',
            'imagem_capa': 'media/capas_campeonato/cidade_vermelha.png',
            'autor_nome': 'Gideon Jura',
            'autor_avatar': 'media/avatares/gideon.png'
        },
        {
            'titulo': 'Só Dinos e Mais Nada, Uhum!',
            'descricao': 'Tá no nome. Se vier encher o saco te lapo a mordida, ou o meu amigo Joãozinho comedor de ovo!',
            'formato': 'Commander',
            'data': '01/07/26',
            'imagem_capa': 'media/capas_campeonato/dinos_magic.png',
            'autor_nome': 'Gishath, Avatar do Sol',
            'autor_avatar': 'media/avatares/gisha.png'
        },
        {
            'titulo': 'Redraft Gótico de Innistrad Muito Goth',
            'descricao': 'Venha de preto.',
            'formato': 'Draft',
            'data': '14/08/26',
            'imagem_capa': 'media/capas_campeonato/pretos.png',
            'autor_nome': 'Liliana Vess',
            'autor_avatar': 'media/avatares/lilia.png'
        }
    ]

    context = {
        'torneios_destacados': torneios_mock
    }
    user = request.user
    return render(request, 'index.html', context)
