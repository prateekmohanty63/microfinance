# Generated by Django 3.1.4 on 2022-02-25 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organizationcustomer'),
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizations.organization'),
        ),
    ]
