# Generated by Django 4.0.1 on 2022-01-22 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_rename_name_picture_nome_remove_picture_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='pais',
            field=models.CharField(default='', max_length=50),
        ),
    ]
