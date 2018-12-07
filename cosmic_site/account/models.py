from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)

    def __str__(self):
        return '{} profile'.format(self.user.username)


class Content(models.Model):
    """
    关注系统
    """
    user_form = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    """
    关注者
    """
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    """
    被关注者
    """
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_form, self.user_to)

