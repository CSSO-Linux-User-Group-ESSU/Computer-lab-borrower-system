# Generated by Django 5.1.1 on 2024-09-27 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrower_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowerinfo',
            name='first_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='borrowerinfo',
            name='last_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='borrowerinfo',
            name='middle_initial',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='borrowerinfo',
            name='projector_qty',
            field=models.CharField(max_length=5),
        ),
    ]