# Generated by Django 2.1.15 on 2022-01-24 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220124_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='transcript',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Transcript'),
        ),
    ]
