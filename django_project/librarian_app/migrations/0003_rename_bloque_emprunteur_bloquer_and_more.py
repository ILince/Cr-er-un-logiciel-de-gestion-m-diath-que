# Generated by Django 5.0.6 on 2024-06-07 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('librarian_app', '0002_emprunteur'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emprunteur',
            old_name='bloque',
            new_name='bloquer',
        ),
        migrations.RenameField(
            model_name='emprunteur',
            old_name='name',
            new_name='nom',
        ),
    ]