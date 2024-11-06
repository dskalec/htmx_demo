from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Todo(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    completed = models.BooleanField(verbose_name=_("Is completed?"), default=False)
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    completed_at = models.DateTimeField(verbose_name=_("Completed at"), null=True, blank=True)

    class Meta:
        verbose_name = _("Todo")
        verbose_name_plural = _("Todos")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @classmethod
    def create_new(cls, title: str, description: str):
        return cls.objects.create(title=title, description=description)

    def complete(self):
        self.completed = True
        self.completed_at = now()
        self.save()

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = now()
        elif not self.completed:
            self.completed_at = None

        super().save(*args, **kwargs)
