# Generated by Django 3.2 on 2021-07-24 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('userchat_opt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userchat_opt', to=settings.AUTH_USER_MODEL)),
                ('userchat_vend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userchat_vend', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, max_length=500, null=True)),
                ('status_timestamp', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('userchar_map_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.userchat')),
            ],
        ),
    ]
