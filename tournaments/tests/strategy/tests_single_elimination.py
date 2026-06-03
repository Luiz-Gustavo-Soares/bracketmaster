from django.test import TestCase
from ...models import Torneio, Rodada, TorneioParticipante
from django.contrib.auth.models import User
from tournaments.enums import StatusRodada, FormatoTorneio
from matches.models import Partida
from matches.enums import ResultadoPartida

class StrategyTestSingleElimination(TestCase):
    def test_pareamento_par(self):
        org = User.objects.create(username='organizador')
        
        t1 = Torneio.objects.create(nome='torn1', formato_torneio=FormatoTorneio.SINGLE_ELIM, numero_rodadas=3, data_inicio='2026-07-12', organizador=org)
        
        jogadores = [User.objects.create(username=f'Jogador_{j}') 
                    for j in range(8)]

        participantes = []
        for jogador in jogadores:
            participantes.append(TorneioParticipante.objects.create(torneio=t1, jogador=jogador))

        rodada1 = Rodada.objects.create(torneio=t1, numero=1)
        t1.strategy.gerar_pareamento(rodada1)

        self.assertEqual(
            len(t1.rodadas.get(numero = 1).partidas.all()), 4
        )  

        partidas = list(Partida.objects.filter(rodada=rodada1))
        for partida in partidas:
            p1, p2 = list(partida.participacoes.all())
            
            p1.resultado = ResultadoPartida.VITORIA
            p2.resultado = ResultadoPartida.DERROTA
            p1.save()
            p2.save()

        rodada2 = Rodada.objects.create(torneio=t1, numero=2)
        
        self.assertEqual(
            len(t1.strategy.gerar_pareamento(rodada2)), 2
        )


    def test_pareamento_impar(self):
        org = User.objects.create(username='organizador')
        
        t1 = Torneio.objects.create(nome='torn1', formato_torneio=FormatoTorneio.SINGLE_ELIM, numero_rodadas=3, data_inicio='2026-07-12', organizador=org)
        
        jogadores = [User.objects.create(username=f'Jogador_{j}') 
                    for j in range(9)]

        participantes = []
        for jogador in jogadores:
            participantes.append(TorneioParticipante.objects.create(torneio=t1, jogador=jogador))

        rodada1 = Rodada.objects.create(torneio=t1, numero=1)
        t1.strategy.gerar_pareamento(rodada1)

        self.assertEqual(
            len(t1.rodadas.get(numero = 1).partidas.all()), 4
        )  

        partidas = list(Partida.objects.filter(rodada=rodada1))
        for partida in partidas:
            p1, p2 = list(partida.participacoes.all())
            
            p1.resultado = ResultadoPartida.VITORIA
            p2.resultado = ResultadoPartida.DERROTA
            p1.save()
            p2.save()

        rodada2 = Rodada.objects.create(torneio=t1, numero=2)
        
        self.assertEqual(
            len(t1.strategy.gerar_pareamento(rodada2)), 2
        )
