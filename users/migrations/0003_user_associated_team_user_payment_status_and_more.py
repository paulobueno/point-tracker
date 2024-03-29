# Generated by Django 4.1.4 on 2023-04-23 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_jump_tags_jump_jump_tags'),
        ('users', '0002_rename_user_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='associated_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.team'),
        ),
        migrations.AddField(
            model_name='user',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='team_name',
            field=models.CharField(default='No Name', max_length=100),
        ),
    ]
