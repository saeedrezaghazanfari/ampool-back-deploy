# Generated by Django 4.0.2 on 2022-06-20 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultingPriceRateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(default=5, verbose_name='تایم ابتدایی')),
                ('price', models.FloatField(default=50000, verbose_name='نرخ ابتدایی - تومان')),
                ('price_2', models.FloatField(default=25000, verbose_name='نرخ پیج دقیقه\u200cی اضافه - تومان')),
            ],
            options={
                'verbose_name': 'نرخ مشاوره',
                'verbose_name_plural': 'نرخ مشاوره',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SendSMSModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='این مقدار فقط در دیتابیس میباشد و برای کاربر ارسال نمیشود', max_length=255, verbose_name='عنوان پیامک')),
                ('content', models.TextField(verbose_name='متن پیامک')),
                ('recievers', models.CharField(choices=[('all', 'همه'), ('patients', 'بیماران'), ('doctors', 'پزشک\u200cها'), ('nurses', 'پرستاران')], default='all', max_length=20, verbose_name='چه کسانی این پیامک را دریافت کنند؟')),
                ('is_send', models.BooleanField(default=False, help_text='اگر این گزینه فعال شد و این رکورد را ذخیره کردید، بلافاصله ارسال پیامک آغاز میشود.', verbose_name='ارسال شود؟')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'پیامک پزشکی',
                'verbose_name_plural': 'پیامک\u200cهای پزشکی',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SettingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_scale', models.FloatField(blank=True, null=True, verbose_name='مقیاس ایکس')),
                ('y_scale', models.FloatField(blank=True, null=True, verbose_name='مقیاس ایگرگ')),
                ('marker_text', models.CharField(blank=True, max_length=50, null=True, verbose_name='متن شما روی نقشه')),
                ('country', models.CharField(blank=True, max_length=50, null=True, verbose_name='کشور')),
                ('state', models.CharField(blank=True, max_length=50, null=True, verbose_name='استان')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='شهرستان')),
                ('phone', models.PositiveBigIntegerField(verbose_name='تلفن')),
                ('from_to', models.CharField(blank=True, max_length=200, null=True, verbose_name='زمان گشایش')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='ایمیل')),
                ('your_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='متن شما درمورد ارتباط')),
            ],
            options={
                'verbose_name': '\u200cتنظیمات',
                'verbose_name_plural': '\u200cتنظیمات',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='UserActionsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('financial', 'امور مالی'), ('medical_advice', 'مشاوره\u200cی پزشکی'), ('recommender', 'توصیه گر'), ('upgrade_ac', 'ارتقای حساب کاربری'), ('change_pw', 'تغییر رمزعبور')], default='financial', max_length=255, verbose_name='نوع اقدام')),
                ('action', models.TextField(blank=True, null=True, verbose_name='شرح اقدام انجام شده')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'اقدام کاربر',
                'verbose_name_plural': 'اقدامات کاربران',
                'ordering': ['-id'],
            },
        ),
    ]
