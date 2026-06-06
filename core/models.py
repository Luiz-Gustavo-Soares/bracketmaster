from django.db import models

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def save(self, *args, **kwargs):
        self.nome = self._normalizar(self.nome)
        self.estado = self._normalizar(self.estado)

        super().save(*args, **kwargs)

    
    def _normalizar(palavra: str) -> str:
        return palavra.strip().title()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nome', 'estado'],
                name='unique_city'
            )
        ]
