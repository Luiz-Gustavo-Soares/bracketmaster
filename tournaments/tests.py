from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from core.exceptions import PermissionDenied
from matches.enums import ResultadoPartida, StatusPartida
from matches.models import Partida
from matches.services.partidada_service import PartidaService
from tournaments.enums import (
    FormatoTorneio,
    StatusInscricao,
    StatusRodada,
    StatusTorneio,
)
from tournaments.models import Rodada, Torneio, TorneioParticipante
from tournaments.services.exceptions import (
    AlreadyRegisteredError,
    InvalidCodeError,
    ParticipantLimitError,
    RegistrationClosedError,
    OpenMatchesError,
)
from tournaments.services.rankinService import RankingService
from tournaments.services.registroService import TournamentRegistrationService
from tournaments.services.torneioService import TournamentService
from tournaments.states.exceptions import InsufficientParticipantsError


class BracketMasterTestCase(TestCase):
    def setUp(self):
        self.organizador = User.objects.create_user(
            username="organizador",
            password="teste123",
        )
        self.jogador_a = User.objects.create_user(
            username="jogador_a",
            password="teste123",
        )
        self.jogador_b = User.objects.create_user(
            username="jogador_b",
            password="teste123",
        )
        self.outro_usuario = User.objects.create_user(
            username="outro_usuario",
            password="teste123",
        )

    def criar_torneio(
        self,
        *,
        formato=FormatoTorneio.SWISS,
        numero_rodadas=2,
        maximo_participantes=8,
        inscricao_publica=True,
    ):
        return Torneio.objects.create(
            nome="Torneio de testes",
            organizador=self.organizador,
            numero_maximo_participantes=maximo_participantes,
            inscricao_publica=inscricao_publica,
            formato_torneio=formato,
            numero_rodadas=numero_rodadas,
            data_inicio=timezone.now() + timedelta(days=1),
        )

    def criar_participantes(self, torneio, quantidade, status=StatusInscricao.APROVADA):
        participantes = []
        for indice in range(quantidade):
            jogador = User.objects.create_user(
                username=f"participante_{indice}",
                password="teste123",
            )
            participantes.append(
                TorneioParticipante.objects.create(
                    torneio=torneio,
                    jogador=jogador,
                    status=status,
                )
            )
        return participantes

    def iniciar_torneio(self, torneio, quantidade_participantes=2):
        self.criar_participantes(torneio, quantidade_participantes)
        TournamentService.abrir_inscricoes(torneio)
        TournamentService.encerrar_inscricoes(torneio)
        TournamentService.iniciar(torneio)
        torneio.refresh_from_db()
        return torneio.rodadas.get(numero=1)


class TournamentRegistrationServiceTests(BracketMasterTestCase):
    def test_jogador_pode_se_inscrever_em_torneio_publico(self):
        torneio = self.criar_torneio()
        TournamentService.abrir_inscricoes(torneio)

        TournamentRegistrationService.adicionar_jogador(torneio, self.jogador_a)

        participante = TorneioParticipante.objects.get(
            torneio=torneio,
            jogador=self.jogador_a,
        )
        self.assertEqual(participante.status, StatusInscricao.PENDENTE)

    def test_nao_permite_inscricao_com_periodo_fechado(self):
        torneio = self.criar_torneio()

        with self.assertRaises(RegistrationClosedError):
            TournamentRegistrationService.adicionar_jogador(torneio, self.jogador_a)

    def test_nao_permite_inscricao_duplicada(self):
        torneio = self.criar_torneio()
        TournamentService.abrir_inscricoes(torneio)
        TorneioParticipante.objects.create(torneio=torneio, jogador=self.jogador_a)

        with self.assertRaises(AlreadyRegisteredError):
            TournamentRegistrationService.adicionar_jogador(torneio, self.jogador_a)

    def test_respeita_limite_de_participantes(self):
        torneio = self.criar_torneio(maximo_participantes=1)
        TournamentService.abrir_inscricoes(torneio)
        TorneioParticipante.objects.create(torneio=torneio, jogador=self.jogador_a)

        with self.assertRaises(ParticipantLimitError):
            TournamentRegistrationService.adicionar_jogador(torneio, self.jogador_b)

    def test_torneio_privado_exige_codigo_correto(self):
        torneio = self.criar_torneio(inscricao_publica=False)
        TournamentService.abrir_inscricoes(torneio)

        with self.assertRaises(InvalidCodeError):
            TournamentRegistrationService.adicionar_jogador(
                torneio,
                self.jogador_a,
                codigo="CODIGO-ERRADO",
            )

        TournamentRegistrationService.adicionar_jogador(
            torneio,
            self.jogador_a,
            codigo=torneio.codigo_inscricao,
        )
        self.assertTrue(
            TorneioParticipante.objects.filter(
                torneio=torneio,
                jogador=self.jogador_a,
            ).exists()
        )

    def test_somente_organizador_pode_aprovar_inscricao(self):
        torneio = self.criar_torneio()
        participante = TorneioParticipante.objects.create(
            torneio=torneio,
            jogador=self.jogador_a,
        )

        with self.assertRaises(PermissionDenied):
            TournamentRegistrationService.approvar_jogador(
                participante,
                self.outro_usuario,
            )

        TournamentRegistrationService.approvar_jogador(participante, self.organizador)
        participante.refresh_from_db()
        self.assertEqual(participante.status, StatusInscricao.APROVADA)

    def test_somente_organizador_pode_rejeitar_inscricao(self):
        torneio = self.criar_torneio()
        participante = TorneioParticipante.objects.create(
            torneio=torneio,
            jogador=self.jogador_a,
        )

        with self.assertRaises(PermissionDenied):
            TournamentRegistrationService.regeitar_jogador(
                participante,
                self.outro_usuario,
            )

        TournamentRegistrationService.regeitar_jogador(participante, self.organizador)
        participante.refresh_from_db()
        self.assertEqual(participante.status, StatusInscricao.REJEITADA)


class TournamentWorkflowTests(BracketMasterTestCase):
    def test_nao_fecha_inscricoes_com_menos_de_dois_participantes(self):
        torneio = self.criar_torneio()
        TorneioParticipante.objects.create(torneio=torneio, jogador=self.jogador_a)
        TournamentService.abrir_inscricoes(torneio)

        with self.assertRaises(InsufficientParticipantsError):
            TournamentService.encerrar_inscricoes(torneio)

    def test_fecha_inscricoes_com_dois_participantes(self):
        torneio = self.criar_torneio()
        self.criar_participantes(torneio, 2)
        TournamentService.abrir_inscricoes(torneio)

        TournamentService.encerrar_inscricoes(torneio)

        torneio.refresh_from_db()
        self.assertEqual(torneio.status, StatusTorneio.INSCRICOES_E)

    def test_iniciar_torneio_suico_cria_primeira_rodada_e_pareamentos(self):
        torneio = self.criar_torneio(formato=FormatoTorneio.SWISS)

        rodada = self.iniciar_torneio(torneio, quantidade_participantes=4)

        self.assertEqual(rodada.status, StatusRodada.ABERTA)
        self.assertEqual(rodada.partidas.count(), 2)
        self.assertEqual(
            sum(partida.participacoes.count() for partida in rodada.partidas.all()),
            4,
        )

    def test_sistema_suico_concede_bye_quando_quantidade_e_impar(self):
        torneio = self.criar_torneio(formato=FormatoTorneio.SWISS)
        rodada = self.iniciar_torneio(torneio, quantidade_participantes=3)

        partidas = list(rodada.partidas.all())
        partidas_com_bye = [partida for partida in partidas if partida.participacoes.count() == 1]

        self.assertEqual(len(partidas), 2)
        self.assertEqual(len(partidas_com_bye), 1)
        self.assertEqual(partidas_com_bye[0].status, StatusPartida.FINALIZADA)
        self.assertEqual(
            partidas_com_bye[0].participacoes.get().resultado,
            ResultadoPartida.VITORIA,
        )

    def test_eliminatoria_simples_nao_deixa_jogador_sem_pareamento(self):
        torneio = self.criar_torneio(formato=FormatoTorneio.SINGLE_ELIM)
        rodada = self.iniciar_torneio(torneio, quantidade_participantes=3)

        partidas = list(rodada.partidas.all())
        partidas_com_bye = [partida for partida in partidas if partida.participacoes.count() == 1]

        self.assertEqual(len(partidas), 2)
        self.assertEqual(len(partidas_com_bye), 1)
        self.assertEqual(partidas_com_bye[0].status, StatusPartida.FINALIZADA)
        self.assertEqual(
            partidas_com_bye[0].participacoes.get().resultado,
            ResultadoPartida.VITORIA,
        )

    def test_nao_gera_proxima_rodada_enquanto_partida_estiver_aberta(self):
        torneio = self.criar_torneio(numero_rodadas=2)
        rodada = self.iniciar_torneio(torneio, quantidade_participantes=2)

        with self.assertRaises(OpenMatchesError):
            TournamentService.proxima_rodada(torneio)

        rodada.refresh_from_db()
        self.assertEqual(rodada.status, StatusRodada.ABERTA)
        self.assertEqual(torneio.rodadas.count(), 1)

    def test_finaliza_torneio_apos_ultima_rodada(self):
        torneio = self.criar_torneio(numero_rodadas=1)
        rodada = self.iniciar_torneio(torneio, quantidade_participantes=2)
        partida = rodada.partidas.get()
        vencedor = partida.participacoes.first()

        PartidaService.registrar_resultado(partida, vencedor)
        PartidaService.finalizar_partida(partida)

        proxima = TournamentService.proxima_rodada(torneio)

        torneio.refresh_from_db()
        rodada.refresh_from_db()
        self.assertIsNone(proxima)
        self.assertEqual(torneio.status, StatusTorneio.FINALIZADO)
        self.assertEqual(rodada.status, StatusRodada.FINALIZADA)

    def test_recalcula_pontuacao_e_estatisticas(self):
        torneio = self.criar_torneio(numero_rodadas=1)
        rodada = self.iniciar_torneio(torneio, quantidade_participantes=2)
        partida = rodada.partidas.get()
        participacao_vencedora = partida.participacoes.first()

        PartidaService.registrar_resultado(partida, participacao_vencedora)
        PartidaService.finalizar_partida(partida)
        RankingService.recalcular(torneio)

        participante_vencedor = TorneioParticipante.objects.get(
            torneio=torneio,
            jogador=participacao_vencedora.jogador,
        )
        participante_perdedor = TorneioParticipante.objects.exclude(
            pk=participante_vencedor.pk,
        ).get(torneio=torneio)

        self.assertEqual(participante_vencedor.pontos, 3)
        self.assertEqual(participante_vencedor.vitorias, 1)
        self.assertEqual(participante_vencedor.derrotas, 0)
        self.assertEqual(participante_perdedor.pontos, 0)
        self.assertEqual(participante_perdedor.derrotas, 1)
