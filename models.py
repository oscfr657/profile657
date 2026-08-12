from django.db import models
from django.utils.text import slugify
from django.contrib.sites.models import Site


class Lock(models.Model):
    startdate = models.DateTimeField(verbose_name='Start date')
    enddate = models.DateTimeField(verbose_name='End date', null=True, blank=True)
    password = models.CharField(
        max_length=128, verbose_name='Password', null=True, blank=True
    )
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name='+', null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if self.password:
            self.password = slugify(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        end_str = (
            self.enddate.strftime('%Y-%m-%d %H:%M') if self.enddate else 'indefinitely'
        )
        return f'Lock ({self.startdate.strftime('%Y-%m-%d %H:%M')} to {end_str})'
