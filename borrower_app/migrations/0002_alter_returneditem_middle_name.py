# Generated by Django 4.2.16 on 2024-11-07 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrower_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='returneditem',
            name='middle_name',
            field=models.CharField(max_length=100),
        ),
    ]