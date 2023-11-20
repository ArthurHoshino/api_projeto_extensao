from django.db import models

# Create your models here.

class Midia(models.IntegerChoices):
    DIGITAL = 0, 'Digital'
    FISICO = 1, 'Fisico'

class Plataforma(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.nome}"

class Loja(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome}"
    
class Produto(models.Model):
    nome = models.CharField(max_length=255)
    precoTotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precoDesconto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)
    midia = models.IntegerField(default=Midia.FISICO, choices=Midia.choices)
    link = models.CharField(max_length=999)
    linkImagem = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.id})"