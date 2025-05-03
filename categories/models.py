from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kategoriya nomi")
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children',
        verbose_name="Ota-kategoriya"
    )
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Kategoriya rasmi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
