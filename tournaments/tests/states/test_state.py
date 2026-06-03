from django.test import TestCase
from ...models import Torneio, Rodada, TorneioParticipante
from django.contrib.auth.models import User
from tournaments.enums import StatusTorneio, StatusRodada

class StateTest(TestCase):
    def test_abrir_insc(self):
        org = User.objects.create(username='organizador')
        
        t1 = Torneio.objects.create(nome='torn1', formato_torneio='SWISS', numero_rodadas=3, data_inicio='2026-07-12', organizador=org)

        self.assertEqual(
            t1.status,
            StatusTorneio.CRIADO
        )

        t1.state.abrir_inscricoes()

        self.assertEqual(
            t1.status,
            StatusTorneio.INSCRICOES
        )


    def test_enc_inscri(self):
        org = User.objects.create(username='organizador')
        
        t1 = Torneio.objects.create(nome='torn1', formato_torneio='SWISS', numero_rodadas=3, data_inicio='2026-07-12', organizador=org)


        t1.state.abrir_inscricoes()


        self.assertRaises(
            RuntimeError,
            t1.state.encerrar_inscricoes
        )

        jogadores = [User.objects.create(username=f'Jogador_{j}') 
                    for j in range(3)]

        for jogador in jogadores:
            TorneioParticipante.objects.create(torneio=t1, jogador=jogador)
        
        t1.state.encerrar_inscricoes()

        self.assertEqual(
            t1.status,
            StatusTorneio.INSCRICOES_E
        )



    def test_iniciar_torn(self):
        org = User.objects.create(username='organizador')
        
        t1 = Torneio.objects.create(nome='torn1', formato_torneio='SWISS', numero_rodadas=3, data_inicio='2026-07-12', organizador=org)


        t1.state.abrir_inscricoes()


        jogadores = [User.objects.create(username=f'Jogador_{j}') 
                    for j in range(3)]

        for jogador in jogadores:
            TorneioParticipante.objects.create(torneio=t1, jogador=jogador)
        
        t1.state.encerrar_inscricoes()
        t1.state.iniciar()

        self.assertEqual(
            t1.status,
            StatusTorneio.EM_ANDAMENTO
        )


    def test_finalizar_torn(self):
        org = User.objects.create(username='organizador')
        
        t1 = Torneio.objects.create(nome='torn1', formato_torneio='SWISS', numero_rodadas=1, data_inicio='2026-07-12', organizador=org)


        t1.state.abrir_inscricoes()


        jogadores = [User.objects.create(username=f'Jogador_{j}') 
                    for j in range(2)]

        for jogador in jogadores:
            TorneioParticipante.objects.create(torneio=t1, jogador=jogador)
        
        t1.state.encerrar_inscricoes()
        t1.state.iniciar()


        self.assertRaises(
            RuntimeError,
            t1.state.finalizar
        )
        rodada = Rodada.objects.create(torneio=t1, numero=1, status=StatusRodada.FINALIZADA)

        t1.state.finalizar()

        self.assertEqual(
            t1.status,
            StatusTorneio.FINALIZADO
        )
