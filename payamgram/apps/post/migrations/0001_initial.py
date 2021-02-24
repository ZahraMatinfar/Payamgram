# Generated by Django 3.1.4 on 2021-02-23 11:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('caption', models.TextField()),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
