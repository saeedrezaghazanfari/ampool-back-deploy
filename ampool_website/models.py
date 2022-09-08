import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from ampool_auth.models import User
from ampool_jobs.models import DoctorModel
from Extentions.utils import jalali_convertor, blog_image_path, get_blog_code


class DoctorNotesModel(models.Model):
    doctor = models.ForeignKey(to=DoctorModel, on_delete=models.CASCADE, verbose_name=_('پزشک'))
    short_title = models.CharField(max_length=100, verbose_name=_('عنوان کوتاه'))
    text = models.TextField(max_length=400, verbose_name=_('متن'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('نوت پزشک')
        verbose_name_plural = _('نوت های پرشکان')

    def __str__(self):
        return self.short_title

    def get_full_name(self):
        return f'{self.doctor.user.first_name} {self.doctor.user.last_name}'
    get_full_name.short_description = _('نام پزشک')


class BlogModel(models.Model):
    slug = models.SlugField(unique=True, default=get_blog_code, verbose_name=_('مقدار در url'))
    image = models.ImageField(upload_to=blog_image_path, null=True, blank=True, verbose_name=_('تصویر'))
    writer = models.ForeignKey(to=DoctorModel, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('نویسنده'), help_text=_('آگر نویسنده ای انتخاب نشود، این پست توسط پشتیبان نوشته شده است'))
    categories = models.ManyToManyField(to='CategoryModel', verbose_name=_('دسته بندی ها'))
    tags = models.ManyToManyField(to='TagModel', verbose_name=_('تگ ها'))
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    desc = models.TextField(verbose_name=_('متن مقاله'))
    short_desc = models.CharField(max_length=500, verbose_name=_('متن کوتاه'))
    is_published = models.BooleanField(default=False, verbose_name=_('منتشر شود؟'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('بلاگ')
        verbose_name_plural = _('بلاگ‌ها')

    def __str__(self):
        return self.title

    def j_created(self):
        return jalali_convertor(time=self.created, output='j_date')
    j_created.short_description = _('تاریخ انتشار')

    def j_month(self):
        return jalali_convertor(time=self.created, output='j_month')

    def prev_post(self):
        prev_id = int(self.id) - 1
        blog = BlogModel.objects.filter(id=prev_id, is_published=True).first()
        if blog:
            return blog
        return None

    def next_post(self):
        next_id = int(self.id) + 1
        blog = BlogModel.objects.filter(id=next_id, is_published=True).first()
        if blog:
            return blog
        return None

    def get_full_name(self):
        try:
            return f'{self.writer.user.first_name} {self.writer.user.last_name}'
        except:
            return _('پشتیبان')
    get_full_name.short_description = _('نام نویسنده')


class CommentModel(models.Model):
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('پاسخ'))
    message = models.TextField(verbose_name=_('نظر'))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    blog = models.ForeignKey(to=BlogModel, on_delete=models.CASCADE, verbose_name=_('بلاگ'))
    created = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False, verbose_name=_('پاسخ؟'))
    is_show = models.BooleanField(default=False, verbose_name=_('نمایش؟'))
    is_read = models.BooleanField(default=False, verbose_name=_('توسط نویسنده خوانده شده؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نظر کاربر')
        verbose_name_plural = _('نظرات کاربران')

    def j_created(self):
        return jalali_convertor(time=self.created, output='j_date')
    j_created.short_description = _('تاریخ نظر')

    def __str__(self):
        return str(self.id)

class CategoryModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')

    def __str__(self):
        return self.title


class TagModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تگ')
        verbose_name_plural = _('تگ ها')

    def __str__(self):
        return self.title


class BlogLikesModel(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    blog = models.ForeignKey(to=BlogModel, on_delete=models.CASCADE, verbose_name=_('بلاگ'))
    
    class Meta:
        ordering = ['-id']
        verbose_name = _('پست و لایک')
        verbose_name_plural = _('پست ها و لایک ها')

    def __str__(self):
        return str(self.id)


class ContactUsModel(models.Model):
    message = models.TextField(verbose_name=_('متن ارتباط'))
    name = models.CharField(max_length=100, verbose_name=_('نام کاربر'))
    email = models.EmailField(max_length=100, verbose_name=_('ایمیل کاربر'))
    title = models.CharField(max_length=100, verbose_name=_('عنوان ارتباط'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('پیام مخاطب')
        verbose_name_plural = _('پیام های مخاطبان')

    def __str__(self):
        return str(self.title)
