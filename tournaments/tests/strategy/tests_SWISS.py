from django.test import TestCase
from ...models import Torneio, Rodada, TorneioParticipante
from django.contrib.auth.models import User
from tournaments.enums import StatusRodada
# Create your tests here.

class TorneioTest(TestCase):
    pass


class StrategyTestSWISS(TestCase):

    # Testa o pareamento no sistema suiço com participantes pares
    def test_pareamento_par(self):
        org = User.objects.create(username='organizador')
        
        t1 = Torneio.objects.create(nome='torn1', formato_torneio='SWISS', numero_rodadas=3, data_inicio='2026-07-12', organizador=org)
        
        jogadores = [User.objects.create(username=f'Jogador_{j}') 
                    for j in range(6)]

        for jogador in jogadores:
            TorneioParticipante.objects.create(torneio=t1, jogador=jogador)

        rodada = Rodada.objects.create(torneio=t1, numero=1)
        t1.strategy.gerar_pareamento(rodada)

        self.assertEqual(
            len(t1.rodadas.get(numero = 1).partidas.all()), 3
        )


    # Testa o pareamento no sistema suiço com participantes impares
    def test_pareamento_impar(self):
        org = User.objects.create(username='organizador')
        
        t1 = Torneio.objects.create(nome='torn1', formato_torneio='SWISS', numero_rodadas=3, data_inicio='2026-07-12', organizador=org)
        
        jogadores = [User.objects.create(username=f'Jogador_{j}') 
                    for j in range(7)]

        for jogador in jogadores:
            TorneioParticipante.objects.create(torneio=t1, jogador=jogador)

        rodada = Rodada.objects.create(torneio=t1, numero=1)
        t1.strategy.gerar_pareamento(rodada)

        self.assertEqual(
            len(t1.rodadas.get(numero = 1).partidas.all()), 4
        )


    def test_pode_criar_nova_rodada(self):
        org = User.objects.create(username='organizador')
    
        t1 = Torneio.objects.create(nome='torn1', formato_torneio='SWISS', numero_rodadas=3, data_inicio='2026-07-12', organizador=org)
        
        jogadores = [User.objects.create(username=f'Jogador_{j}') 
                    for j in range(7)]

        for jogador in jogadores:
            TorneioParticipante.objects.create(torneio=t1, jogador=jogador)

        rodada1 = Rodada.objects.create(torneio=t1, numero=1)
        
        self.assertFalse(
            t1.strategy.pode_criar_proxima_rodada()
        )

       
        rodada1.status = StatusRodada.FINALIZADA
        rodada1.save()

        self.assertTrue(
            t1.strategy.pode_criar_proxima_rodada()
        )

        rodada2 = Rodada.objects.create(torneio=t1, numero=2)
        rodada3 = Rodada.objects.create(torneio=t1, numero=3)
        self.assertFalse(
            t1.strategy.pode_criar_proxima_rodada()
        )

        rodada2.status = StatusRodada.FINALIZADA
        rodada2.save()
        rodada3.status = StatusRodada.FINALIZADA
        rodada3.save()

        self.assertFalse(
            t1.strategy.pode_criar_proxima_rodada()
        )


    def test_terminou(self):
        org = User.objects.create(username='organizador')
    
        t1 = Torneio.objects.create(nome='torn1', formato_torneio='SWISS', numero_rodadas=2, data_inicio='2026-07-12', organizador=org)
        
        jogadores = [User.objects.create(username=f'Jogador_{j}') 
                    for j in range(4)]

        for jogador in jogadores:
            TorneioParticipante.objects.create(torneio=t1, jogador=jogador)

        rodada1 = Rodada.objects.create(torneio=t1, numero=1)
        
        self.assertFalse(
            t1.strategy.terminou()
        )

        rodada2 = Rodada.objects.create(torneio=t1, numero=2)
        rodada1.status = StatusRodada.FINALIZADA
        rodada1.save()
        self.assertFalse(
            t1.strategy.terminou()
        )

        rodada2.status = StatusRodada.FINALIZADA
        rodada2.save()
        self.assertTrue(
            t1.strategy.terminou()
        )
