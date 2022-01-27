# Generated by Django 4.0.1 on 2022-01-20 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('raw_material', '0001_initial'),
        ('material', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='pickupmaterial',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pick_up_material_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pickupmaterial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='material.material'),
        ),
        migrations.AddField(
            model_name='materialcategory',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='material_category_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='materialcategory',
            name='update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material_category_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='material',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='material.materialcategory'),
        ),
        migrations.AddField(
            model_name='material',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='material_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='material',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='raw_material.unit'),
        ),
        migrations.AddField(
            model_name='material',
            name='update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='addmaterial',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='add_material_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='addmaterial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='material.material'),
        ),
        migrations.AddField(
            model_name='addmaterial',
            name='update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='add_material_update_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
