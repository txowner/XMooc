# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-03 15:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20171225_1804'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='课程机构'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否轮播'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='教师'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=DjangoUeditor.models.UEditorField(verbose_name='课程详情'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, max_length=128, null=True, upload_to='courses/%Y/%m',
                                    verbose_name='封面图'),
        ),
    ]
