# Generated by Django 4.1.9 on 2023-06-05 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_last_day_menstraution_cycletracking_last_day_menstruation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cycletracking',
            old_name='last_day_menstruation',
            new_name='last_menstruation_start',
        ),
    ]