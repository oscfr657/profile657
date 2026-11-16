from django.db import models
from django.utils.text import slugify
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

User = get_user_model()


class Key(models.Model):
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name='+', null=True, blank=True
    )
    startdate = models.DateTimeField(verbose_name='Start date')
    enddate = models.DateTimeField(verbose_name='End date', null=True, blank=True)
    password = models.CharField(
        max_length=128, verbose_name='Password', null=True, blank=True
    )
    invites = models.PositiveIntegerField(
        null=True, blank=True, help_text="Number of invites. Leave empty for unlimitet."
    )

    def save(self, *args, **kwargs):
        if self.password:
            self.password = slugify(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        end_str = (
            self.enddate.strftime('%Y-%m-%d %H:%M') if self.enddate else 'indefinitely'
        )
        return f'Key ({self.startdate.strftime('%Y-%m-%d %H:%M')} to {end_str})'


class PasswordDelegation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+')
    trusted_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return (
            f"{self.trusted_user.username} manages passwords for {self.user.username}"
        )


class Service(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='+')
    name = models.CharField(max_length=255, verbose_name="Service name")
    slug = models.SlugField(blank=True)
    subscribers = models.ManyToManyField(
        User,
        related_name='+',
        verbose_name="Subscribers",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('name', 'site'), ('slug', 'site'))
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.site.domain})"
