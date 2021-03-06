# Generated by Django 3.0.3 on 2020-03-05 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0006_remove_component_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='component_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='component',
            name='component_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.EmailField(default=None, max_length=100),
        ),
    ]
