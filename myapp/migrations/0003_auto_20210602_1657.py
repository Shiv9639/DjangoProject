# Generated by Django 3.2.3 on 2021-06-02 20:57

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='length',
            field=models.IntegerField(default=12),
        ),
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='student',
            name='province',
            field=models.CharField(default='ON', max_length=2),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.IntegerField(choices=[(0, 'Cancelled'), (1, 'Confirmed'), (2, 'On Hold')], default=1, max_length=1)),
                ('order_date', models.DateField(default=datetime.datetime(2021, 6, 2, 20, 57, 58, 924245, tzinfo=utc))),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.student')),
                ('courses', models.ManyToManyField(to='myapp.Course')),
            ],
        ),
    ]
