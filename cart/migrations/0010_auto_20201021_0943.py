# Generated by Django 3.1.1 on 2020-10-21 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_order_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='county',
            field=models.CharField(blank=True, default='county', max_length=80),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_reference',
            field=models.CharField(max_length=36),
        ),
        migrations.AlterField(
            model_name='order',
            name='postcode',
            field=models.CharField(blank=True, default='postcode', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='street_address2',
            field=models.CharField(blank=True, default='sa1', max_length=80),
            preserve_default=False,
        ),
    ]