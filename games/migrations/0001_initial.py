# Generated by Django 5.1.7 on 2025-03-09 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pre-started', 'Pre-started'), ('started', 'Started'), ('ended', 'Ended')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('current_round', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='GameQuestion',
            fields=[
                ('question_number', models.IntegerField(primary_key=True, serialize=False)),
                ('start_time_for_user1', models.DateTimeField(blank=True, null=True)),
                ('start_time_for_user2', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.IntegerField(default=1)),
                ('count_of_passed_users', models.IntegerField(default=0)),
                ('user1_score', models.IntegerField(default=0)),
                ('user2_score', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
