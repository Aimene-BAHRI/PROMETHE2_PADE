# Generated by Django 3.1.5 on 2021-01-21 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multicritere', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(blank=True, choices=[(1, 'Coordinateur'), (2, 'Decideur')], max_length=20, null=True),
        ),
    ]
