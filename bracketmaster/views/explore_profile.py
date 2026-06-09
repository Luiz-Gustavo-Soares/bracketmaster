from django.shortcuts import render
from django.core.paginator import Paginator

class MockPerfil:
    def __init__(self, username, nickname, elo_nome, elo_classe, pontos, location, bio, winrate, total_torneios, rank_position, image_path=None):
        # Simula o relacionamento perfil.user.username exigido pelo HTML
        self.user = type('MockUser', (object,), {'username': username})()
        self.nickname = nickname
        self.elo_nome = elo_nome
        self.elo_classe = elo_classe
        self.pontos = pontos
        self.location = location
        self.bio = bio
        self.winrate = winrate
        self.total_torneios = total_torneios
        self.rank_position = rank_position
        
        # Simula o comportamento de um campo de imagem (.url)
        if image_path:
            self.profile_imagem = type('MockImage', (object,), {'url': image_path})()
        else:
            self.profile_imagem = None

def explore_profile(request):
    # 1. Criação dos perfis de teste com os dados alinhados com o universo do Magic
    p1 = MockPerfil("NissaRevane", "Nissa R.", "Challenger", "challenger", 2850, "Belo Horizonte, MG", "Procurando sempre a sinergia perfeita entre os terrenos e o grimório. Foco em formatos competitivos.", 74, 45, 1, "/static/media/avatares/nissa.png")
    p2 = MockPerfil("GideonJura", "Gideon J.", "Platina", "platinum", 2100, "São Paulo, SP", "Justiça nas chaves e foco total no formato Modern. Campeão do Open de Araras.", 62, 38, 2, "/static/media/avatares/gideon.png")
    p3 = MockPerfil("LaysaMagic", "Laysa M.", "Diamante", "diamond", 1950, "Diamantina, MG", "Casal Magic na vida real e Commander mesão aos finais de semana. Control player nata.", 68, 25, 3)
    p4 = MockPerfil("LordCalabreso", "Calabreso", "Ouro", "gold", 1450, "Rio de Janeiro, RJ", "Se não for para cometer loucuras com um deck mono-red aggro eu nem saio de casa.", 55, 18, 4)
    p5 = MockPerfil("ChandraNalaar", "Chandra N.", "Ouro", "gold", 1300, "Curitiba, PR", "Queimando turnos na velocidade da luz e triturando pontos de vida desde 2024.", 58, 22, 5)
    p6 = MockPerfil("JaceBeleren", "Jace B.", "Platina", "platinum", 1750, "Manaus, AM", "Sim, eu vou gastar todas as minhas anulações na sua mágica principal. Aceite o counter.", 60, 30, 6)

    # Base completa de perfis para alimentar o loop principal
    lista_perfis = [p1, p2, p3, p4, p5, p6]
    
    # O pódio espera exatamente uma lista ordenada com os 3 melhores
    top_profiles = [p1, p2, p3]

    # 2. Configuração do Paginator para quebrar a lista de 4 em 4 perfis
    # Assim você consegue testar o sumiço/aparecimento dos botões de paginação nas abas construídas
    paginator = Paginator(lista_perfis, 4)
    page_number = request.GET.get('page')
    perfis_paginados = paginator.get_page(page_number)

    context = {
        'top_profiles': top_profiles,
        'perfis': perfis_paginados,
    }

    return render(request, 'explore_profile.html', context)