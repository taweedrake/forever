# Generated by Django 4.1.3 on 2022-12-07 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_userprofile_allow_chats_private_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='allow_chats_private',
            field=models.BooleanField(default=False, help_text='Allow those who have targeted you to chat with you', verbose_name='Allow Private Chats'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='allow_chats_public',
            field=models.BooleanField(default=False, help_text='Allow anyone to chat with you even if you are not Targetting eachother', verbose_name='Allow Public Chats'),
        ),
    ]
