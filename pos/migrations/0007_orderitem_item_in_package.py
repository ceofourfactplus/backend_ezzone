# Generated by Django 4.0.1 on 2022-01-24 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0006_alter_orderitem_status_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='item_in_package',
            field=models.BooleanField(default=False),
        ),
    ]
