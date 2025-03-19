# Generated by Django 5.0.7 on 2025-01-26 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('basic_info', models.TextField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
