# Generated by Django 3.0.3 on 2020-05-30 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200530_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Post date'),
        ),
    ]