# Generated by Django 4.1 on 2025-04-09 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("octofit_tracker", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="leaderboard",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="team",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="workout",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
