# Generated by Django 4.0.2 on 2022-04-01 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0005_nametemplate_stage_actually_date_stage_is_pass_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicwork',
            name='is_complited',
            field=models.BooleanField(default=False),
        ),
    ]
