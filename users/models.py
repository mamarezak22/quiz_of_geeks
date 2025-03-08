from django.db import models

class TelegramUser(models.Model):
    numeric_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.numeric_id

class TelegramUserAnswerHistory(models.Model):
    telegram_user = models.ForeignKey("TelegramUser", on_delete=models.CASCADE)
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE)
    user_answer = models.ForeignKey("questions.Answer", on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now=True)


