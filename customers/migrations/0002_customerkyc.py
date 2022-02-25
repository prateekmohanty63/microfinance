# Generated by Django 3.1.4 on 2022-02-25 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerKYC',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_kyc_id', models.CharField(blank=True, max_length=32)),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('birth_date', models.DateTimeField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('phone_number', models.CharField(blank=True, max_length=25)),
                ('national_id', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('archived', 'Archived'), ('deleted', 'Deleted')], default='active', max_length=25)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.customer')),
            ],
        ),
    ]
