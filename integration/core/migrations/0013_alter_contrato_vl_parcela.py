# Generated by Django 3.2.4 on 2023-07-21 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_despesa_dt_vencimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='vl_parcela',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
