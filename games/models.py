from django.db import models

class Game(models.Model):
    game_statuses = (
        ('active', 'Active'),
        ('ended', 'Ended'),
    )
    user1 = models.ForeignKey("users.User", on_delete=models.PROTECT,related_name='games')
    user2 = models.ForeignKey("users.User", on_delete=models.PROTECT,related_name='games')
    game_status = models.CharField(max_length=10,choices=game_statuses)
    started_at = models.DateTimeField(auto_now_add =True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.user1} vs {self.user2}'

class GameRound(models.Model):
    round_number = models.IntegerField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='rounds')

class GameQuestion(models.Model):
    question_number = models.IntegerField(primary_key=True)
    round = models.ForeignKey(GameRound, on_delete=models.PROTECT, related_name='questions')
    question = models.ForeignKey("questions.Question", on_delete=models.PROTECT)
    user1_answer = models.ForeignKey("questions.Answer", on_delete=models.PROTECT)
    user2_answer = models.ForeignKey("questions.Answer", on_delete=models.PROTECT)



class GameResult(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    user1_score = models.IntegerField()
    user2_score = models.IntegerField()
    def __str__(self):
        return f'{self.game.user1} : {self.user1_score} - {self.game.user2} : {self.user2_score}'

    @property
    def winner(self):
        has_ended = self.game.status == 'ended'
        if has_ended:
            if self.user1_score > self.user2_score:
                return self.game.user1
            return self.game.user2

