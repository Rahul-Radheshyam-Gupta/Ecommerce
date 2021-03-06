# Generated by Django 3.1.7 on 2021-05-09 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_productdetail_productfeatures_productreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='auth_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
