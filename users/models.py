from django.db import models

class TelegramUser(models.Model):
    numeric_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.numeric_id

class UserHistory(models.Model):
    user = models.ForeignKey("TelegramUser", on_delete=models.CASCADE)
    count_of_won_games = models.IntegerField(default=0)
    count_of_lose_games = models.IntegerField(default=0)
    count_of_correct_answer = models.IntegerField(default=0)

    def __str__(self):
        return f'history of {self.user}'

