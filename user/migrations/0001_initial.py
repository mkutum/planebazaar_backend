# Generated by Django 3.2 on 2021-07-24 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_name', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('password', models.CharField(max_length=250)),
                ('contact_number', models.PositiveIntegerField(blank=True, null=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('designation', models.CharField(max_length=300)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('inactive_timestamp', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Blacklisted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('inactive_timestamp', models.DateTimeField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=250)),
                ('org_type', models.CharField(choices=[('OPERATOR', 'Operator'), ('VENDOR', 'Vendor')], default='OPERATOR', max_length=250)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('location', models.CharField(blank=True, max_length=250, null=True)),
                ('email', models.EmailField(max_length=250)),
                ('contact_number', models.PositiveIntegerField(blank=True, null=True)),
                ('area_of_operation', models.CharField(blank=True, max_length=250, null=True)),
                ('year_of_estb', models.DateField()),
                ('about_organisation', models.CharField(blank=True, max_length=500, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('website', models.URLField(blank=True, max_length=300, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('inactive_timestamp', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=True)),
                ('inactive_timestamp', models.DateTimeField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('org_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='user.organisation')),
            ],
        ),
        migrations.CreateModel(
            name='OrgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('inactive_timestamp', models.DateTimeField(max_length=100)),
                ('created_time', models.DateField(auto_now_add=True)),
                ('org_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userorg', to='user.organisation')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orguser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OperatorVendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('inactive_timestamp', models.DateTimeField(max_length=100)),
                ('orgid_opt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Orgopt', to='user.organisation')),
                ('orgid_vend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to='user.organisation')),
            ],
        ),
        migrations.CreateModel(
            name='OperatorVendChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('edited_by_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='privatelist_change', to=settings.AUTH_USER_MODEL)),
                ('optvend_map_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operatorvendchange', to='user.operatorvendor')),
            ],
        ),
        migrations.CreateModel(
            name='BlacklistedChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('blacklisted_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacklistedchange', to='user.blacklisted')),
                ('edited_by_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacklisted_change_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='blacklisted',
            name='orgid_opt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacklisted_by', to='user.organisation'),
        ),
        migrations.AddField(
            model_name='blacklisted',
            name='orgid_vend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacklisteds', to='user.organisation'),
        ),
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('year_of_manufacture', models.CharField(max_length=250)),
                ('manufacturer', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=True)),
                ('inactive_timestamp', models.DateTimeField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('org_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircrafts', to='user.organisation')),
            ],
        ),
    ]
