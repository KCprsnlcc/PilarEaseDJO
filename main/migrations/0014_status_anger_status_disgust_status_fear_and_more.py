# Generated by Django 5.0.6 on 2024-07-31 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_status_confidence_scores'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='anger',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='status',
            name='disgust',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='status',
            name='fear',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='status',
            name='happiness',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='status',
            name='sadness',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='status',
            name='surprise',
            field=models.FloatField(default=0.0),
        ),
    ]