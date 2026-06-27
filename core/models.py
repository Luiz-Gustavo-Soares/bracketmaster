from django.db import models

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def save(self, *args, **kwargs):
        self.nome = self._normalizar(self.nome)
        self.estado = self._normalizar(self.estado)

        super().save(*args, **kwargs)

    @property
    def str_city(self):
        return f'{self.nome}, {self.estado.upper()}'
    
    @staticmethod
    def _normalizar(palavra: str) -> str:
        return palavra.strip().title()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nome', 'estado'],
                name='unique_city'
            )
        ]


class Endereco(models.Model):
    lagradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=120)
    complemento = models.CharField(max_length=200, blank=True, null=True)

    @property
    def str_local(self):
        return f'{self.lagradouro} - {self.numero}, {self.bairro}' + (f', {self.complemento}' if self.complemento else '')
