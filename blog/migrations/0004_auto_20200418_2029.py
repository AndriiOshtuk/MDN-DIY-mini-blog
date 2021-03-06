# Generated by Django 3.0.3 on 2020-04-18 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200418_2024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['post_date']},
        ),
        migrations.AddField(
            model_name='post',
            name='blogger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Blogger'),
        ),
    ]
