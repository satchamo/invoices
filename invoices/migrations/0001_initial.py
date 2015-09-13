# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_id', models.AutoField(serialize=False, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('tax', models.DecimalField(default=0, decimal_places=2, max_digits=10)),
                ('fk', models.CharField(max_length=255)),
                ('charge_id', models.CharField(max_length=255)),
                ('card', models.CharField(max_length=255)),
                ('app', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['created_on'],
                'db_table': 'invoice',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('invoice_item_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(default=1)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('taxable', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'invoice_item',
                'managed': False,
            },
        ),
        migrations.RunSQL("""
            CREATE VIEW invoice AS SELECT * FROM Invoice.invoice;
            CREATE VIEW invoice_item AS SELECT * FROM Invoice.invoice_item;
        """)
    ]
