# Generated by Django 3.2 on 2021-07-24 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('performa', models.URLField(blank=True, null=True)),
                ('po', models.URLField(blank=True, null=True)),
                ('final_invoice', models.URLField(blank=True, null=True)),
                ('inactive_timestamp', models.DateTimeField(default=False)),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component_type', models.CharField(choices=[('PART', 'PART'), ('CONSUMABLE', 'Consumable')], max_length=200)),
                ('created_time', models.DateField(auto_now_add=True)),
                ('added_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components_added_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=500)),
                ('status', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('flaged_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_type', models.CharField(max_length=255)),
                ('unit_price', models.PositiveIntegerField()),
                ('manufacturer', models.CharField(max_length=255)),
                ('serial_number', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('component_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='component_pricing', to='rfq.component')),
            ],
        ),
        migrations.CreateModel(
            name='Rfq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfq_type', models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private')], default='Public', max_length=250)),
                ('short_description', models.CharField(blank=True, max_length=300, null=True)),
                ('attachment', models.URLField(blank=True, max_length=300, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('draft_status', models.BooleanField(default=False)),
                ('rfq_value', models.PositiveIntegerField()),
                ('priority', models.CharField(choices=[('NORMAL', 'Normal'), ('AOG', 'AOG'), ('PRIORITY', 'Priority')], default='Normal', max_length=250)),
                ('is_dead', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('orguser_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rfq_user', to='user.orguser')),
            ],
        ),
        migrations.CreateModel(
            name='Rfqs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('target_date', models.DateField()),
                ('inactive_timestamp', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('added_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadline_edited_by', to=settings.AUTH_USER_MODEL)),
                ('rfq_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rfq_deadline', to='rfq.rfq')),
            ],
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quotation', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('tax', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('shipping_cost', models.IntegerField(blank=True, null=True)),
                ('quotation_closed', models.BooleanField(default=False)),
                ('delivery_date', models.DateField(default=False)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('orguser_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='user.orguser')),
                ('rfq_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rfq', to='rfq.rfq')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('edited_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('rfq_attachment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rfq.attachment')),
            ],
        ),
        migrations.CreateModel(
            name='PricingChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.PositiveIntegerField()),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('edited_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pricing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pricing_change', to='rfq.pricing')),
            ],
        ),
        migrations.AddField(
            model_name='pricing',
            name='quotation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation_pricing', to='rfq.quotation'),
        ),
        migrations.CreateModel(
            name='Parts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_name', models.CharField(blank=True, max_length=300, null=True)),
                ('part_number', models.IntegerField()),
                ('description', models.TextField(max_length=300)),
                ('manufacturer', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('certifications', models.TextField(blank=True, max_length=500, null=True)),
                ('created_time', models.DateField(auto_now_add=True)),
                ('added_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('component_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='rfq.component')),
            ],
        ),
        migrations.CreateModel(
            name='FlagChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('flag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flag_changed', to='rfq.flag')),
                ('flaged_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='flag',
            name='quotation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flagedrfq', to='rfq.quotation'),
        ),
        migrations.CreateModel(
            name='Consumable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumable_name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=300)),
                ('quantity', models.PositiveIntegerField()),
                ('quantity_type', models.CharField(max_length=100)),
                ('consumable_number', models.IntegerField()),
                ('certifications', models.TextField(blank=True, max_length=500, null=True)),
                ('created_time', models.DateField(auto_now_add=True)),
                ('added_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('component_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='consumables', to='rfq.component')),
            ],
        ),
        migrations.AddField(
            model_name='component',
            name='rfq_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='componet_for_rfq', to='rfq.rfq'),
        ),
        migrations.CreateModel(
            name='Bookmarkquote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('bookmarked_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('quotation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarkedquote', to='rfq.quotation')),
            ],
        ),
        migrations.AddField(
            model_name='attachment',
            name='quotation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rfqquotes', to='rfq.quotation'),
        ),
    ]
