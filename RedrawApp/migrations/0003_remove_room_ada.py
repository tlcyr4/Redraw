# Generated by Django 2.0 on 2018-04-21 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RedrawApp', '0002_remove_building_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='ada',
        ),
    ]
