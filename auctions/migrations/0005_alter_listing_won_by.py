# Generated by Django 4.1 on 2022-10-09 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_closed_listing_created_by_listing_won_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='won_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listing_won', to=settings.AUTH_USER_MODEL),
        ),
    ]
