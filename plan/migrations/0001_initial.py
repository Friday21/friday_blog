# Generated by Django 2.1.2 on 2018-10-27 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_type', models.SmallIntegerField(choices=[(1, '日计划'), (4, '周计划'), (2, '月计划'), (3, '年计划')], default=1, verbose_name='计划类型')),
                ('title', models.CharField(max_length=128, verbose_name='计划名称')),
                ('content', models.TextField(max_length=1024, verbose_name='计划内容')),
                ('finish_status', models.SmallIntegerField(choices=[(1, '非常不满'), (2, '不满意'), (3, '凑合'), (4, '满意')], default=1, verbose_name='满意程度')),
                ('is_finish', models.BooleanField(default=False, verbose_name='是否完成')),
                ('event_time', models.SmallIntegerField(blank=True, choices=[(1, '早上'), (2, '上午'), (3, '下午'), (4, '晚上')], null=True, verbose_name='计划时间段')),
                ('date', models.DateField(blank=True, null=True, verbose_name='计划日期')),
                ('week', models.SmallIntegerField(blank=True, choices=[(1, '第一周'), (2, '第二周'), (3, '第三周'), (4, '第四周'), (5, '第五周')], null=True, verbose_name='周')),
                ('month', models.SmallIntegerField(blank=True, choices=[(1, '一月'), (2, '二月'), (3, '三月'), (4, '四月'), (5, '五月'), (6, '六月'), (7, '七月'), (8, '八月'), (9, '九月'), (10, '十月'), (11, '十一月'), (12, '十二月')], null=True, verbose_name='月份')),
                ('year', models.SmallIntegerField(blank=True, default=2018, null=True, verbose_name='年份')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='类型')),
            ],
            options={
                'verbose_name': '事件类型',
                'verbose_name_plural': '事件类型',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.EventType', verbose_name='内容分类'),
        ),
        migrations.CreateModel(
            name='DailyPlan',
            fields=[
            ],
            options={
                'verbose_name': '日计划',
                'verbose_name_plural': '日计划',
                'proxy': True,
                'indexes': [],
            },
            bases=('plan.event',),
        ),
        migrations.CreateModel(
            name='MonthPlan',
            fields=[
            ],
            options={
                'verbose_name': '月计划',
                'verbose_name_plural': '月计划',
                'proxy': True,
                'indexes': [],
            },
            bases=('plan.event',),
        ),
        migrations.CreateModel(
            name='WeekPlan',
            fields=[
            ],
            options={
                'verbose_name': '周计划',
                'verbose_name_plural': '周计划',
                'proxy': True,
                'indexes': [],
            },
            bases=('plan.event',),
        ),
        migrations.CreateModel(
            name='YearPlan',
            fields=[
            ],
            options={
                'verbose_name': '年计划',
                'verbose_name_plural': '年计划',
                'proxy': True,
                'indexes': [],
            },
            bases=('plan.event',),
        ),
    ]
