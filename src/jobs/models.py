from django.db import models
from cloudinary.models import CloudinaryField


class Location(models.TextChoices):
    DELEGACION = 'delegacion', 'Delegación'
    FARMACIA = 'farmacia', 'Farmacia'
    OPTICA = 'optica', 'Óptica'
    OTRO = 'otro', 'Otro'


class Job(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=30, choices=Location.choices)
    duration = models.PositiveIntegerField(help_text='Duración en minutos')
    description = models.TextField(blank=True, help_text='Descripción del trabajo')
    tags = models.ManyToManyField('Tag', blank=True, related_name='jobs')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Trabajo'
        verbose_name_plural = 'Trabajos'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} - {self.location}"
    

class JobPhoto(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='photos')
    photo = CloudinaryField('image', folder='job_photos/', resource_type='image',)
    before_after = models.CharField(max_length=6, choices=[('before', 'Antes'), ('after', 'Después')])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto de Trabajo'
        verbose_name_plural = 'Fotos de Trabajos'

    def __str__(self):
        return f"{self.job} - {self.before_after}"
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['name']

    def __str__(self):
        return f"#{self.name}"