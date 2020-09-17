# Generated by Django 3.0.2 on 2020-09-16 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20200916_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='medication',
            name='receiver',
            field=models.ForeignKey(default=32, on_delete=django.db.models.deletion.CASCADE, related_name='medicationreceiver', to=settings.AUTH_USER_MODEL, verbose_name='receiver'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medication',
            name='sender',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='medicationsender', to='backend.Doctor', verbose_name='sender'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patient',
            name='medication',
            field=models.ManyToManyField(related_name='medication', to='backend.Medication', verbose_name='medication'),
        ),
    ]
