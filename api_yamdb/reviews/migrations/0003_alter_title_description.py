# Generated by Django 3.2 on 2023-06-09 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230607_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(null=True),
        ),
    ]