# Generated by Django 4.1 on 2022-08-12 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_recruit_total_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(unique=True)),
                ('recruit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.recruit')),
            ],
        ),
        migrations.CreateModel(
            name='SelectTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fixed', models.BooleanField(default=False)),
                ('apply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.apply')),
                ('select_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.timetable')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('view_range', models.IntegerField(default=0)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.club')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.manager')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('line_idx', models.IntegerField(default=0)),
                ('apply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.apply')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.manager')),
            ],
        ),
        migrations.CreateModel(
            name='ApplyForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.club')),
            ],
        ),
    ]