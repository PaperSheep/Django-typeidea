# Generated by Django 2.1.2 on 2019-05-09 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_comment_html'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='comment_html',
            new_name='content_html',
        ),
    ]