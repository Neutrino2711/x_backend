# Generated by Django 4.2.10 on 2024-03-19 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='commentvote',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='commentvote',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='commentvote',
            name='user',
        ),
        migrations.AddField(
            model_name='post',
            name='depth',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='post.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='CommentVote',
        ),
    ]