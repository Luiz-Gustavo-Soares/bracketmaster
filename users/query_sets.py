from django.db import models
from django.db.models import Count, Q, F, FloatField
from django.db.models import ExpressionWrapper, Case, When, Value

from matches.enums import ResultadoPartida

    
class PerfilQuerySet(models.QuerySet):

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