# Generated by Django 3.1.3 on 2020-11-24 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botmain', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servers',
            name='levels',
            field=models.BooleanField(default='False', verbose_name='Leveling and autoroles'),
        ),
    ]
