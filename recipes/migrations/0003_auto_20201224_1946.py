# Generated by Django 3.1.4 on 2020-12-24 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20201224_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='duration',
            field=models.PositiveIntegerField(verbose_name='Время приготовления'),
        ),
    ]
