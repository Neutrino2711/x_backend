# Generated by Django 4.2.10 on 2024-03-24 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_commentvote_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hastag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='hastags',
            field=models.ManyToManyField(blank=True, to='post.hastag'),
        ),
    ]