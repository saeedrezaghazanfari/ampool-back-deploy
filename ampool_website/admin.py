from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    DoctorNotesModel,
    BlogModel,
    CategoryModel,
    TagModel,
    CommentModel,
    BlogLikesModel,
    ContactUsModel,
)

class DoctorNotesModel_Admin(admin.ModelAdmin):
    list_display = ['short_title', 'get_full_name']
    search_field = ['short_title', 'get_full_name']
    ordering = ['-id']

class ContactUsModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'email']
    ordering = ['-id']

class BlogModel_Admin(admin.ModelAdmin):
    list_display = ['slug', 'get_full_name', 'is_published', 'j_created']
    search_field = ['slug', 'get_full_name', 'is_published']
    ordering = ['-id']

class CategoryModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']

class TagModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']

class CommentModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'j_created', 'is_show']
    ordering = ['-id']

admin.site.register(DoctorNotesModel, DoctorNotesModel_Admin)
admin.site.register(BlogModel, BlogModel_Admin)
admin.site.register(CategoryModel, CategoryModel_Admin)
admin.site.register(TagModel, TagModel_Admin)
admin.site.register(CommentModel, CommentModel_Admin)
admin.site.register(BlogLikesModel)
admin.site.register(ContactUsModel, ContactUsModel_Admin)