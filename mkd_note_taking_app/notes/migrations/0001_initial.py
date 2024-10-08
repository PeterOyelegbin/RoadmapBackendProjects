# Generated by Django 5.1.1 on 2024-09-11 17:45

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MarkDown',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('filename', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='./mkd_note_taking_app/static/md_files/')),
            ],
        ),
    ]
