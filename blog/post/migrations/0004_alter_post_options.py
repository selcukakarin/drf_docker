# Generated by Django 5.0.6 on 2024-09-18 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_modified_by_alter_post_created_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
    ]