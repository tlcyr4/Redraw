# Generated by Django 2.0 on 2018-04-23 13:46

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('number', models.CharField(max_length=4, unique=True)),
                ('coordinates', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('res_college', models.BooleanField()),
                ('upperclass', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=2)),
                ('dimensions', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RedrawApp.Building')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draw_time', models.DateTimeField()),
                ('members', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), size=None)),
                ('drawing_in', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='RedrawApp.Draw')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groups', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), size=5)),
                ('favorites', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), size=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.CharField(max_length=6)),
                ('sqft', models.PositiveSmallIntegerField()),
                ('num_occupants', models.PositiveSmallIntegerField()),
                ('num_rooms', models.PositiveSmallIntegerField(null=True)),
                ('sub_free', models.NullBooleanField()),
                ('draw_rank', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), size=5)),
                ('size_rank', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), size=5)),
                ('polygons', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('draws_in', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='RedrawApp.Draw')),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RedrawApp.Floor')),
            ],
        ),
        migrations.AddField(
            model_name='building',
            name='draw',
            field=models.ManyToManyField(to='RedrawApp.Draw'),
        ),
    ]
