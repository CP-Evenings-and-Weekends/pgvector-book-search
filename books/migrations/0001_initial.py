from django.db import migrations, models
from pgvector.django import VectorExtension
import pgvector.django.vector


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        VectorExtension(), # must add this extension manually

        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255),
                ),
                (
                    "author",
                    models.CharField(max_length=255),
                ),
                (
                    "description",
                    models.TextField(),
                ),
                (
                    "embedding",
                    pgvector.django.vector.VectorField(
                        blank=True,
                        dimensions=768,
                        null=True,
                    ),
                ),
            ],
        ),
    ]