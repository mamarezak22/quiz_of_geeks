from django.db import models

class Game(models.Model):
    #user 1 means the first user that goes in searching for a game.
    game_statuses = (
        ('pre-started', 'Pre-started'),
        ('started', 'Started'),
        ('ended', 'Ended'),
    )
    user1 = models.ForeignKey("users.User", on_delete=models.SET_NULL,related_name='game_as_user1',blank=True,null=True)
    user2 = models.ForeignKey("users.User", on_delete=models.SET_NULL,related_name='game_as_user2',blank=True, null=True)
    status = models.CharField(max_length=20,choices=game_statuses)
    created_at = models.DateTimeField(auto_now_add =True)
    ended_at = models.DateTimeField(blank=True, null=True)
    # 0 means we are in pre-started status
    current_round = models.IntegerField(default = 1)


    def __str__(self):
        return f'{self.user1} vs {self.user2}'

class GameRound(models.Model):
    round_number = models.IntegerField(default = 1)
    game = models.ForeignKey("Game", on_delete=models.PROTECT, related_name='rounds')
    selected_category = models.ForeignKey("questions.Category", on_delete=models.PROTECT)
    count_of_passed_users = models.IntegerField(default=0)
    user1_score = models.IntegerField(default=0)
    user2_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add =True)

    @property
    #1 as return value means user1 and 2 as user2.
    def starter_user(self):
        if self.round_number %2 == 0:
            return 2
        return 1
    @property
    #the property that clears what user turn is now.
    #if returns 1 means user1 and 2 for user2.
    def turn(self):
        if self.starter_user == 1:
            if self.count_of_passed_users == 0:
                return 1
            return 2
        else:
            if self.count_of_passed_users == 0:
                return 2
            return 1



    def save(self, *args, **kwargs):
        # we only want set things diffrent when creating a object. and in that time object does not have a pk.
        if not self.pk:
            last_round = GameRound.objects.filter(game=self.game).order_by('-round_number').first()
            #there is any before round set the value one more.
            #if not the default value is 1.
            if last_round:
                self.round_number = last_round.round_number + 1
        super().save(*args, **kwargs)


class GameQuestion(models.Model):
    question_number = models.IntegerField(primary_key=True)
    round = models.ForeignKey(GameRound, on_delete=models.PROTECT, related_name='questions')
    question = models.ForeignKey("questions.Question", on_delete=models.PROTECT)
    user1_answer = models.ForeignKey("questions.Answer", on_delete=models.PROTECT,blank = True, null=True,related_name='answer_as_user1')
    user2_answer = models.ForeignKey("questions.Answer", on_delete=models.PROTECT,blank = True, null=True,related_name='answer_as_user2')
    start_time_for_user1 = models.DateTimeField(blank=True, null=True)
    start_time_for_user2 = models.DateTimeField(blank=True, null=True)


