# Generated by Django 3.2.9 on 2021-11-26 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_alter_item_list'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('list', 'text')},
        ),
    ]