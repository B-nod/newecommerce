# Generated by Django 5.0.4 on 2024-04-19 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_order_contact_no_alter_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Cash on delivery', 'Cash on delivery'), ('Esewa', 'Esewa')], default=1, max_length=200),
        ),
    ]
