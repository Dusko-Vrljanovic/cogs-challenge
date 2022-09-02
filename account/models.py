from django.db import models
from django.contrib.auth.models import User as DjangoUser, AbstractUser
# Create your models here.


class User(AbstractUser):
    screen_name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        ordering = ['username']
        db_table = 'user'

    @property
    def user_screen_name(self):
        return self.screen_name or self.username

    def __str__(self):
        return self.user_screen_name
