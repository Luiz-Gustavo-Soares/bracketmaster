from django.db import models
from django.db.models import Count, Q

from tournaments.enums import StatusInscricao

    
class TorneioQuerySet(models.QuerySet):

    def com_participantes_validos_count(self):
        return self.annotate(
            participantes_validos_count=Count(
                "participantes",
                filter=Q(participantes__status=StatusInscricao.APROVADA),
                distinct=True,
            )
        )
    
class ParticipanteQuerySet(models.QuerySet):
    def aprovados(self):
        return self.filter(
            status=StatusInscricao.APROVADA
        )
