# Generated by Django 2.2.3 on 2021-05-26 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0003_auto_20210526_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulo',
            name='img_mostrador',
            field=models.ImageField(default='https://st3.depositphotos.com/2927609/32461/v/600/depositphotos_324611040-stock-illustration-no-image-vector-icon-no.jpg', upload_to='Producto_mostrador'),
        ),
    ]