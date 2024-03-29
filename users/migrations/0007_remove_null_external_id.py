# Generated by Django 4.1.4 on 2023-05-28 20:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_populate_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='external_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        )
    ]
