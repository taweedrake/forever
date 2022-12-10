from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,DeleteView
from django.contrib import messages
from .models import BlogPost



class BlogView(ListView):
    model=BlogPost
    template_name='blog/bloglist.html'
    ordering = ['-date']

class BlogDetailView(DetailView):
    model=BlogPost
    template_name='blog/blogdetail.html'
    def get_context_data(self, **kwargs):
        blog_name=self.kwargs['blogname']
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        post =  BlogPost.objects.get(pk = self.kwargs['pk'])
        author_posts = BlogPost.objects.filter(author = post.author.id).exclude(title=blog_name).order_by('-date')
        context["posts"] = author_posts
        return context

class AddPostView(CreateView):
    model=BlogPost
    template_name='blog/addpost.html'
    fields=['title','body','image','category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PreDeleteView(ListView):
    template_name = 'blog/predelete.html'
    model = BlogPost

    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        # filter by a variable captured from url, for example
        return qs.filter(author_id=self.kwargs['pk']).order_by('-date')

class PostDeleteView(DeleteView):
    model = BlogPost
    template_name='blog/deletepost.html'

    success_url=reverse_lazy('addpost')