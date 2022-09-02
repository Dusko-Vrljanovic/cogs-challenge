from django.db import models
from django.contrib.auth.models import User as DjangoUser
# Create your models here.
from django.utils.timezone import now


class User(DjangoUser):
    screen_name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        ordering = ['username']
        db_table = 'user'

    @property
    def user_screen_name(self):
        return self.screen_name or self.username

    def __str__(self):
        return self.user_screen_name
