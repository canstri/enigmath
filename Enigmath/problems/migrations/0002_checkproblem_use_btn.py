# Generated by Django 2.0.1 on 2018-02-14 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkproblem',
            name='use_btn',
            field=models.BooleanField(default=False),
        ),
    ]
