# Generated by Django 3.0.5 on 2020-04-20 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='messageQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ename', models.CharField(max_length=50, verbose_name='英文名')),
                ('cname', models.CharField(default='', max_length=10, null=True, verbose_name='中文名')),
                ('compan', models.CharField(default='', max_length=50, null=True, verbose_name='公司')),
            ],
            options={
                'verbose_name': '消息队列',
                'verbose_name_plural': '消息队列',
                'db_table': 'message_queue',
                'unique_together': {('ename', 'cname')},
                'index_together': {('ename', 'cname')},
            },
        ),
    ]
