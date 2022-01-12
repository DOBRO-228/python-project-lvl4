# Generated by Django 3.2.11 on 2022-01-12 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0004_alter_status_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Status', 'verbose_name_plural': 'Statuses'},
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Name'),
        ),
    ]
