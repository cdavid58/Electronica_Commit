# Generated by Django 2.2.3 on 2021-07-29 19:42

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0005_articulo_newproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='color',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('green', 'VERDE'), ('blue', 'AZUL'), ('red', 'ROJO'), ('orange', 'ANARANJADO'), ('black', 'NEGRO'), ('pink', 'ROSA')], default='green', max_length=700, null=True),
        ),
    ]