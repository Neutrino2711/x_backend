# Generated by Django 4.2.10 on 2024-03-12 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]