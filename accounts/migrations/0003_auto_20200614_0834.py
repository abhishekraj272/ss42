# Generated by Django 2.2.3 on 2020-06-14 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_authentication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authentication',
            name='token',
            field=models.CharField(blank=True, max_length=35),
        ),
    ]
