from .base_strategy import BaseStrategy
from matches.models import Partida, ParticipacaoPartida
from matches.enums import ResultadoPartida
from tournaments.enums import StatusRodada



class SingleEliminationStrategy(BaseStrategy):
    """Torneio Formato Eliminatoria simples"""
    def _get_jogadores_vivos(self):
        """Busca todos os jogadores ainda vivos
        Returns:
            List[participantes ainda vivos]
            """

        participantes = self.torneio.participantes.aprovados.all()

        vivos = []

        for p in participantes:
                perdeu = Partida.objects.filter(
                        rodada__torneio=self.torneio,
                        participacoes__jogador=p.jogador,
                        participacoes__resultado=ResultadoPartida.DERROTA
                    ).exists()

                if not perdeu:
                    vivos.append(p)

        return vivos

    def gerar_pareamento(self, rodada):
        '''Gera o pareamento do sistema de Eliminatoria simples
        Args:
            rodada: Rodada
                Rodada a ser gerada o pareamento
        Return:
            list partidas criadas para essa rodada
        '''

        jogadores = self._get_jogadores_vivos()

        partidas = []

        while len(jogadores) >= 2:

            p1 = jogadores.pop(0)
            p2 = jogadores.pop(0)

            partida = Partida.objects.create(
                rodada=rodada
            )

            ParticipacaoPartida.objects.create(
                partida=partida,
                jogador=p1.jogador
            )

            ParticipacaoPartida.objects.create(
                partida=partida,
                jogador=p2.jogador
            )

            partidas.append(partida)

        # if jogadores:
        #     p = jogadores.pop(0)
        #     partida = Partida.objects.create(rodada=rodada)
        #     ParticipacaoPartida.objects.create(
        #         partida=partida,
        #         jogador=p.jogador
        #     )
        #     # partida.finalizar_partida(p.jogador) tem que ver como modelar isso ainda se o bye vai ser uma partidad solo
        #     partidas.append(partida)
        
        return partidas


    def pode_criar_proxima_rodada(self):
        """Verifica se o torneio esta apto a criar uma nova rodada"""
        
        if self.torneio.rodadas.count() >= self.torneio.numero_rodadas:
            return False
        
        for rodada in self.torneio.rodadas.all():
            if rodada.status == StatusRodada.ABERTA:
                return False
        
        return True
    
    def terminou(self):
        """Verifica se o torneio terminou"""

        if self.torneio.rodadas.count() < self.torneio.numero_rodadas:
            return False
        
        for rodada in self.torneio.rodadas.all():
            if rodada.status == StatusRodada.ABERTA:
                return False
        
        return True
