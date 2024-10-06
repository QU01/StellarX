from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    title = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user}:{self.title}"

class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, default=None, on_delete=models.CASCADE)
    user_response = models.TextField(null=True, default='')
    ai_response = models.TextField(null=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversation}: {self.id}"

# Create your models here.
class Exoplaneta(models.Model):
    constelacion = models.CharField(max_length=100)
    distancia_light_years = models.FloatField()
    exoplaneta = models.CharField(max_length=100)
    masa = models.FloatField(null=True, blank=True)  # en masas terrestres
    radio = models.FloatField(null=True, blank=True)  # en radios terrestres
    luz = models.CharField(max_length=100, null=True, blank=True)
    periodo_orbital = models.FloatField(null=True, blank=True)
    fecha_descubrimiento = models.DateField(null=True, blank=True)
    metodo_deteccion = models.CharField(max_length=100, null=True, blank=True)
    planeta_central = models.CharField(max_length=100, null=True, blank=True)
    sistema_solar = models.CharField(max_length=100, null=True, blank=True)
    tipo_estrella = models.CharField(max_length=100, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.exoplaneta
    
    class Meta:
        verbose_name = "Exoplaneta"
        verbose_name_plural = "Exoplanetas"
        ordering = ["exoplaneta"]

