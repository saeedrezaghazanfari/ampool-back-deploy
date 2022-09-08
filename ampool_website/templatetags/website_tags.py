from django import template
from ampool_jobs.models import DoctorModel
from ampool_website.models import (
    DoctorNotesModel,
    CategoryModel,
    BlogModel
)

register = template.Library()

@register.simple_tag
def doctor_notes():
    notes = DoctorNotesModel.objects.all()[:6]
    if notes:
        return notes
    return None

@register.simple_tag
def last_categories():
    categories_numblogs = []
    categories = CategoryModel.objects.all()
    if categories:
        for category in categories:
            categories_numblogs.append({
                'category_name': category.title, 
                'num': category.blogmodel_set.count()
            })
        return categories_numblogs
    return None
    
@register.simple_tag
def last_posts():
    blogs = BlogModel.objects.filter(is_published=True).all()[:4]
    if blogs:
        return blogs
    return None