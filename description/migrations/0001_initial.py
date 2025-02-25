# Generated by Django 5.1.6 on 2025-02-17 12:45

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sku_id', models.CharField(db_index=True, max_length=15)),
                ('tone', models.CharField(max_length=50)),
                ('language', models.CharField(max_length=25)),
                ('exclude_keywords', models.JSONField()),
                ('include_keywords', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('sku_id', 'tone', 'language'), name='unique_prompt')],
            },
        ),
        migrations.CreateModel(
            name='GeneratedDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('prompt', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='description', to='description.prompt')),
            ],
        ),
    ]
