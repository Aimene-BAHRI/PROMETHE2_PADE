# Generated by Django 3.1.5 on 2021-02-27 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multicritere', '0004_auto_20210220_0909'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataCordinateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mp', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='DataDecideur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weights', models.FileField(upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(blank=True, choices=[('Coordinateur', 'Coordinateur'), ('Decideur', 'Decideur')], max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='Data',
        ),
        migrations.AddField(
            model_name='datadecideur',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasDecid', to='multicritere.profile'),
        ),
        migrations.AddField(
            model_name='datacordinateur',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasCord', to='multicritere.profile'),
        ),
    ]