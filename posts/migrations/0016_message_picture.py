# Generated by Django 3.0 on 2020-04-22 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_remove_message_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='picture',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='fake_picture'),
        ),
    ]
