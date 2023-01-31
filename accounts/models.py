from django.contrib.auth.models import User
from django.db import models

from polls.models import Batch


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    batch = models.ForeignKey(Batch, on_delete=models.DO_NOTHING, related_name='batch_students')

    def __str__(self):
        return f'{self.batch.name}-{self.user.username}'
