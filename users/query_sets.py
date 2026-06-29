from django.db import models
from django.db.models import Count, Q, F, FloatField
from django.db.models import ExpressionWrapper, Case, When, Value

from matches.enums import ResultadoPartida
from tournaments.enums import StatusInscricao

    
class PerfilQuerySet(models.QuerySet):

    def com_total_likes(self):
        return self.annotate(
            total_likes=Count(
                'user__likes_recebidos',
                distinct=True
            )
        )
    
    def com_torneios_count(self):
        return self.annotate(
            torneios_count=Count(
                "user__torneioparticipante",
                filter=Q(
                    user__torneioparticipante__status=StatusInscricao.APROVADA
                )
            )
        )

    def com_taxa_vitoria(self):

        return self.annotate(

            total_partidas=Count(
                'user__participacoes',
                distinct=True
            ),

            total_vitorias=Count(
                'user__participacoes',
                filter=Q(
                    user__participacoes__resultado=ResultadoPartida.VITORIA
                ),
                distinct=True
            )

        ).annotate(

            taxa_vitoria=Case(

                When(
                    total_partidas=0,
                    then=Value(0.0)
                ),

                default=ExpressionWrapper(

                    F('total_vitorias') * 100.0 /
                    F('total_partidas'),

                    output_field=FloatField()

                ),

                output_field=FloatField()
            )
        )