# Generated by Django 3.1.3 on 2020-11-16 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rareserverapi', '0002_auto_20201112_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttag',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagging', to='rareserverapi.post'),
        ),
        migrations.AlterField(
            model_name='posttag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagging', to='rareserverapi.tag'),
        ),
    ]
