# Generated by Django 5.1.7 on 2025-03-09 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
        ('questions', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='user1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_as_user1', to='users.user'),
        ),
        migrations.AddField(
            model_name='game',
            name='user2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_as_user2', to='users.user'),
        ),
        migrations.AddField(
            model_name='gamequestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='questions.question'),
        ),
        migrations.AddField(
            model_name='gamequestion',
            name='user1_answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='answer_as_user1', to='questions.answer'),
        ),
        migrations.AddField(
            model_name='gamequestion',
            name='user2_answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='answer_as_user2', to='questions.answer'),
        ),
        migrations.AddField(
            model_name='gameround',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rounds', to='games.game'),
        ),
        migrations.AddField(
            model_name='gameround',
            name='selected_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='questions.category'),
        ),
        migrations.AddField(
            model_name='gamequestion',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='games.gameround'),
        ),
    ]
