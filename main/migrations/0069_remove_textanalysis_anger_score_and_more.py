# Generated by Django 5.0.6 on 2024-10-18 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0068_textanalysis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textanalysis',
            name='anger_score',
        ),
        migrations.RemoveField(
            model_name='textanalysis',
            name='disgust_score',
        ),
        migrations.RemoveField(
            model_name='textanalysis',
            name='fear_score',
        ),
        migrations.RemoveField(
            model_name='textanalysis',
            name='happiness_score',
        ),
        migrations.RemoveField(
            model_name='textanalysis',
            name='neutral_score',
        ),
        migrations.RemoveField(
            model_name='textanalysis',
            name='sadness_score',
        ),
        migrations.RemoveField(
            model_name='textanalysis',
            name='surprise_score',
        ),
    ]
