# Generated by Django 2.1.15 on 2022-01-23 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_transcript_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcript',
            name='grade_courses',
            field=models.ManyToManyField(blank=True, null=True, related_name='grade_courses', to='core.CourseGrade'),
        ),
    ]
