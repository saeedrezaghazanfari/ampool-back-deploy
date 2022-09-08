from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from ampool_setting.models import SettingModel
from ampool_jobs.models import DoctorModel, DoctorDegreeModel
from .models import BlogModel, CommentModel, BlogLikesModel, ContactUsModel
from .forms import CommentForm


# url: /
class IndexPage(generic.TemplateView):
    template_name = 'ampool_website/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = BlogModel.objects.filter(is_published=True).all()[:3]
        list_blogs = []
        for blog in blogs:
            comments = CommentModel.objects.filter(blog=blog, is_reply=False, is_show=True).count()
            replies = CommentModel.objects.filter(blog=blog, is_reply=True, is_show=True).count()

            list_blogs.append({
                'blog':blog, 
                'likes': BlogLikesModel.objects.filter(blog=blog).count(),
                'comments': comments + replies
            })
        context['doctors'] = DoctorModel.objects.filter(is_active=True).all()[:10]
        context['last_blogs'] = list_blogs
        return context


# url: /doctors
class DoctorsPage(generic.TemplateView):
    template_name = 'ampool_website/doctors_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('name') or self.request.GET.get('skill'):
            context['doctors'] = []
            name = self.request.GET.get('name').lower()
            # skill = self.request.GET.get('skill').lower()
            if name:
                lookup1 = Q(user__first_name__icontains=name.split(' ')[0])
                try:
                    lookup2 = Q(user__last_name__icontains=name.split(' ')[1])
                    context['doctors'] += DoctorModel.objects.filter(lookup1, lookup2, is_active=True).all()
                except:
                    context['doctors'] += DoctorModel.objects.filter(lookup1, is_active=True).all()
            # if skill:
            #     degrees = DoctorDegreeModel.objects.filter(skill_title__title=skill).all()
            #     print(degrees)
            #     for degree in degrees:
            #         print(degree)
            #         context['doctors'] += degree.doctor

        else:
            context['doctors'] = DoctorModel.objects.filter(is_active=True).all()
        return context
    

# url: /blogs
class BlogsPage(generic.ListView):
    template_name = 'ampool_website/blogs_page.html'
    model = BlogModel
    def get_queryset(self):
        blogs = BlogModel.objects.filter(is_published=True).all()
        blogs_comments = []
        for blog in blogs:
            comments = CommentModel.objects.filter(blog=blog, is_reply=False, is_show=True).count()
            replies = CommentModel.objects.filter(blog=blog, is_reply=True, is_show=True).count()
            blogs_comments.append({
                'blog': blog,
                'num_comments': comments + replies
            })
        return blogs_comments
    paginate_by = 3


# url: /blogs/like/<slug:slug>
class BlogLikePage(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            this_blog = BlogModel.objects.get(slug=kwargs['slug'])
            exist = BlogLikesModel.objects.filter(user=request.user, blog=this_blog).first()

            if not exist:
                like = BlogLikesModel.objects.create(user=request.user, blog=this_blog)
                if like:
                    likes = BlogLikesModel.objects.filter(blog=this_blog).count()
                    return JsonResponse({'counter': likes, 'status': 200}, safe=False)
            
            elif exist:
                dislike = BlogLikesModel.objects.get(user=request.user, blog=this_blog).delete()
                if dislike:
                    likes = BlogLikesModel.objects.filter(blog=this_blog).count()
                    return JsonResponse({'counter': likes, 'status': 203}, safe=False)

        return JsonResponse({'status': 404}, safe=False)


# url: /blogs/<slug:slug>
class BlogDetailPage(LoginRequiredMixin, generic.DetailView):
    model = BlogModel
    context_object_name = 'blog'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thispost = context['object']
        context['form'] = CommentForm()                                                                            # send form
        context['comments'] = CommentModel.objects.filter(blog=thispost, is_reply=False, is_show=True)             # send comments
        context['replies'] = CommentModel.objects.filter(blog=thispost, is_reply=True, is_show=True)               # send replyes
        context['is_like'] = bool(BlogLikesModel.objects.filter(blog=thispost, user=self.request.user).first())    # like it?     
        context['comments_nums'] = context['comments'].count() + context['replies'].count()                                      # send comments numbers
        context['likes'] = BlogLikesModel.objects.filter(blog=thispost).count()                                                # send likes numbers

        return context
    template_name = 'ampool_website/blog_detail.html'


# url: /blogs/comment/save 
class CommentSaveURL(LoginRequiredMixin, generic.View):
    def post(self, request):
        msg = request.POST['message']
        blog_slug = request.POST['at_blog']
        reply = request.POST['isreply']
        comment_id = request.POST['commentid']

        if msg and blog_slug and reply == 'False' and comment_id == '':
            blog = BlogModel.objects.filter(slug=blog_slug).first()
            comment = CommentModel.objects.create(message=msg, user=request.user, blog=blog)
            if comment and blog:
                messages.success(request, _('نظر شما ثبت شد. بعد از تایید در سایت نمایش خواهد شد'))
                return redirect(f'/blogs/{blog_slug}')
            
            messages.success(request, _('مشکلی به وجود آمده است'))
            return redirect('/')

        elif msg and blog_slug and reply == 'True' and comment_id:
            blog = BlogModel.objects.filter(slug=blog_slug).first()
            comment = CommentModel.objects.get(id=comment_id)
            reply = CommentModel.objects.create(reply=comment, message=msg, user=request.user, blog=blog, is_reply=True)
            if reply and blog:
                messages.success(request, _('پاسخ شما ثبت شد. بعد از تایید در سایت نمایش خواهد شد'))
                return redirect(f'/blogs/{blog_slug}')

            messages.success(request, _('مشکلی به وجود آمده است'))
            return redirect('/')


# url: /blogs/search/
class SearchBoxURL(generic.ListView):
    template_name = 'ampool_website/blogs_page.html'
    model = BlogModel
    paginate_by = 3
    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        lookup = Q(title__icontains=query) | Q(short_desc__icontains=query) | Q(writer__user__first_name__icontains=query)  | Q(writer__user__last_name__icontains=query) 
        blogs = BlogModel.objects.filter(lookup, is_published=True).distinct()

        blogs_comments = []
        for blog in blogs:
            counter = blog.commentmodel_set.filter(is_show=True).count()
            blogs_comments.append({'blog': blog, 'num_comments': counter})
        return blogs_comments

# url: /blogs/search/tags
class SearchTagURL(generic.ListView):
    template_name = 'ampool_website/blogs_page.html'
    model = BlogModel
    paginate_by = 3
    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        blogs = BlogModel.objects.filter(tags__title__iexact=query, is_published=True).distinct()
        blogs_comments = []
        for blog in blogs:
            counter = blog.commentmodel_set.filter(is_show=True).count()
            blogs_comments.append({'blog': blog, 'num_comments': counter})
        return blogs_comments


# url: /blogs/search/categories

class SearchCategoryURL(generic.ListView):
    template_name = 'ampool_website/blogs_page.html'
    model = BlogModel
    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        blogs = BlogModel.objects.filter(categories__title__iexact=query, is_published=True).distinct()
        blogs_comments = []
        for blog in blogs:
            counter = blog.commentmodel_set.filter(is_show=True).count()
            blogs_comments.append({'blog': blog, 'num_comments': counter})
        return blogs_comments
    paginate_by = 3


# url: /contact-us
class ContactUsPage(SuccessMessageMixin, generic.CreateView):
    template_name = 'ampool_website/contactus.html'
    model = ContactUsModel
    success_url = reverse_lazy('website:index')
    fields = ['message', 'name', 'email', 'title']
    success_message = _('با موفقیت پیام شما ارسال شد. سپاس از همراهی شما')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sets'] = SettingModel.objects.first()
        return context
