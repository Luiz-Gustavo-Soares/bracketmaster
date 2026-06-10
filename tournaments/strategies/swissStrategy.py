from .base_strategy import BaseStrategy
from matches.models import Partida, ParticipacaoPartida
from tournaments.enums import StatusRodada

class SwissStrategy(BaseStrategy):
    """Torneio Formato suiço"""

    def gerar_pareamento(self, rodada):
        '''Gera o pareamento do sistema suiço
        Args:
            rodada: Rodada
                Rodada a ser gerada o pareamento
        Return:
            list partidas criadas para essa rodada
        '''

        jogadores = list(
            self.torneio.participantes.aprovados().order_by(
                '-pontos'
            )
        )

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

        if jogadores:
            p = jogadores.pop(0)
            partida = Partida.objects.create(rodada=rodada)
            ParticipacaoPartida.objects.create(
                partida=partida,
                jogador=p.jogador
            )
            # partida.finalizar_partida(p.jogador) tem que ver como modelar isso ainda se o bye vai ser uma partidad solo
            partidas.append(partida)
        
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
