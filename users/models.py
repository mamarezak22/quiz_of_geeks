from django.db import models

class TelegramUser(models.Model):
    numeric_id = models.IntegerField(primary_key=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numeric_id

class UserGameStats(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    count_of_won_games = models.IntegerField(default=0)
    count_of_loss_games = models.IntegerField(default=0)
    count_of_ties = models.IntegerField(default=0)


class UserAnswerHistory(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE)
    is_correct_answer = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

class UserGameHistory(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    game = models.ForeignKey('games.Game',on_delete=models.PROTECT)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} score'



