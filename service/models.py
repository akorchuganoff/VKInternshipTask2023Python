from django.contrib.auth.models import User
from django.db import models


class OutgoingRequests(models.Model):
    from_user_id = models.IntegerField(blank=False)
    to_user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class IngoingRequests(models.Model):
    to_user_id = models.IntegerField(blank=False)
    from_user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
