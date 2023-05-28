# Generated by Django 4.1.4 on 2023-05-28 20:16
import uuid

from django.db import migrations


def gen_uuid(apps, schema_editor):
    my_model = apps.get_model('users', 'User')
    for row in my_model.objects.all():
        row.external_id = uuid.uuid4()
        row.save(update_fields=['external_id'])


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0005_add_external_id_to_user'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
