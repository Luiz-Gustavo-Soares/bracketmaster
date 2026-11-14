from django.contrib.auth.models import User
from django.test import TestCase

from matches.enums import ResultadoPartida, StatusPartida
from matches.models import Partida, ParticipacaoPartida
from matches.services.exceptions import (
    MatchNotFinishedError,
    ParticipatDoesNotInMatchError,
)
from matches.services.partidada_service import PartidaService


class PartidaServiceTests(TestCase):
    def setUp(self):
        self.jogador_a = User.objects.create_user(username="jogador_a", password="teste123")
        self.jogador_b = User.objects.create_user(username="jogador_b", password="teste123")
        self.partida = Partida.objects.create()

        self.participacao_a = ParticipacaoPartida.objects.create(
            partida=self.partida,
            jogador=self.jogador_a,
        )
        self.participacao_b = ParticipacaoPartida.objects.create(
            partida=self.partida,
            jogador=self.jogador_b,
        )

    def test_registrar_vitoria_define_vencedor_e_perdedor(self):
        PartidaService.registrar_resultado(self.partida, self.participacao_a)

        self.participacao_a.refresh_from_db()
        self.participacao_b.refresh_from_db()

        self.assertEqual(self.participacao_a.resultado, ResultadoPartida.VITORIA)
        self.assertEqual(self.participacao_b.resultado, ResultadoPartida.DERROTA)

    def test_registrar_empate_define_empate_para_todos(self):
        PartidaService.registrar_resultado(self.partida)

        self.participacao_a.refresh_from_db()
        self.participacao_b.refresh_from_db()

        self.assertEqual(self.participacao_a.resultado, ResultadoPartida.EMPATE)
        self.assertEqual(self.participacao_b.resultado, ResultadoPartida.EMPATE)

    def test_nao_aceita_participacao_de_outra_partida(self):
        outra_partida = Partida.objects.create()
        participacao_externa = ParticipacaoPartida.objects.create(
            partida=outra_partida,
            jogador=User.objects.create_user(username="jogador_c", password="teste123"),
        )

        with self.assertRaises(ParticipatDoesNotInMatchError):
            PartidaService.registrar_resultado(self.partida, participacao_externa)

    def test_finalizar_partida_altera_status(self):
        PartidaService.finalizar_partida(self.partida)

        self.partida.refresh_from_db()
        self.assertEqual(self.partida.status, StatusPartida.FINALIZADA)

    def test_ganhador_retorna_vencedor_de_partida_finalizada(self):
        PartidaService.registrar_resultado(self.partida, self.participacao_a)
        PartidaService.finalizar_partida(self.partida)

        vencedor = PartidaService.ganhador(self.partida)

        self.assertEqual(vencedor.pk, self.participacao_a.pk)

    def test_ganhador_retorna_none_em_empate(self):
        PartidaService.registrar_resultado(self.partida)
        PartidaService.finalizar_partida(self.partida)

        self.assertIsNone(PartidaService.ganhador(self.partida))

    def test_nao_consulta_ganhador_de_partida_nao_finalizada(self):
        with self.assertRaises(MatchNotFinishedError):
            PartidaService.ganhador(self.partida)
