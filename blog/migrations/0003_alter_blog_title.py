# Generated by Django 5.1.3 on 2024-12-05 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blog_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(default='', max_length=240, unique=True),
        ),
    ]
