from django.db import models

class TelegramUser(models.Model):
    numeric_id = models.IntegerField(primary_key=True)