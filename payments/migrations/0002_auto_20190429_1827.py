# Generated by Django 2.1.1 on 2019-04-29 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoices',
            options={'ordering': ['date_created']},
        ),
    ]
