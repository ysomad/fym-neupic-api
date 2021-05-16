# Generated by Django 3.2.3 on 2021-05-16 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20210516_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='state',
            field=models.CharField(choices=[('edited_image', 'Edited'), ('unedited_image', 'Unedited'), ('template_video', 'Template')], default='unedited_image', max_length=16),
        ),
    ]
