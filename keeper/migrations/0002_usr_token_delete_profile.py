# Generated by Django 4.1.5 on 2023-01-07 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keeper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='usr_token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('token', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
