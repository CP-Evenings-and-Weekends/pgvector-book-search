from django.db import models
from pgvector.django import VectorField


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.TextField()
    description = models.TextField()
    embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        return self.title