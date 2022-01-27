# Generated by Django 4.0.1 on 2022-01-20 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('raw_material', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='toppingcategory',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='topping_category_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='toppingcategory',
            name='update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='topping_category_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topping',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='topping_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topping',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='raw_material.unit'),
        ),
        migrations.AddField(
            model_name='topping',
            name='update_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='topping_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='settopping',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.toppingcategory'),
        ),
        migrations.AddField(
            model_name='settopping',
            name='topping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.topping'),
        ),
        migrations.AddField(
            model_name='salechannel',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sale_channel_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='salechannel',
            name='update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sale_channel_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_category_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_category_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='old_product',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='topping_category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.toppingcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='raw_material.unit'),
        ),
        migrations.AddField(
            model_name='product',
            name='update_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pricetopping',
            name='old_price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.pricetopping'),
        ),
        migrations.AddField(
            model_name='pricetopping',
            name='sale_channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.salechannel'),
        ),
        migrations.AddField(
            model_name='pricetopping',
            name='topping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.topping'),
        ),
        migrations.AddField(
            model_name='priceproduct',
            name='old_price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.priceproduct'),
        ),
        migrations.AddField(
            model_name='priceproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='priceproduct',
            name='sale_channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.salechannel'),
        ),
        migrations.AddField(
            model_name='addproduct',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='add_product_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='addproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product'),
        ),
        migrations.AddField(
            model_name='addproduct',
            name='update_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='add_product_update_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
