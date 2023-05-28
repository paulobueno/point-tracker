# Generated by Django 4.1.4 on 2023-05-28 20:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_associated_team_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='external_id',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]