from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            verbose_name="Status name")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="created at")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Statuses"
        verbose_name_plural = "Statuses"
