# Generated by Django 3.1.4 on 2022-02-25 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organizationcustomer'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('multiple_loans_per_customer', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizations.organization')),
            ],
        ),
    ]
