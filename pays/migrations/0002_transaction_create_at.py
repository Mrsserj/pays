# Generated by Django 3.0.8 on 2020-07-17 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pays', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
    ]
