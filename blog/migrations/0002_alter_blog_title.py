# Generated by Django 5.1.3 on 2024-12-05 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(default='', max_length=240),
        ),
    ]
