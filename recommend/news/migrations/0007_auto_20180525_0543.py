# Generated by Django 2.0.5 on 2018-05-25 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_newskeyword'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'managed': False},
        ),
        migrations.RenameField(
            model_name='newskeyword',
            old_name='keywordId',
            new_name='keyword',
        ),
        migrations.RenameField(
            model_name='newskeyword',
            old_name='newId',
            new_name='news',
        ),
    ]
