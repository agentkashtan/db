# Generated by Django 4.0.4 on 2022-04-28 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', 'test_db'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads'),
        ),
    ]
