# Generated by Django 2.2.1 on 2019-05-08 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='attachment',
            field=models.ImageField(blank=True, null=True, upload_to='attachement'),
        ),
    ]
