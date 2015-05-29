# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alarma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('tipo', models.CharField(default=b'A', max_length=2, choices=[(b'B', b'Nivel muy bajo detectado!'), (b'A', b'Nivel muy alto detectado!')])),
                ('medidor', models.ForeignKey(to='rango.Medidor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
