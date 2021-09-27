from django.db import models

# Create your models here.


class CustomBaseModel(models.Model):
    """Summary Line
    Abstract Class to registry creation date, modify date and is active status of models
    """

    created = models.DateTimeField(auto_now_add=True, db_column="fecha_creacion")
    modified = models.DateTimeField(auto_now=True, db_column="fecha_modificacion")
    is_active = models.BooleanField(default=True, db_column="esta_activo")

    class Meta:
        abstract = True
