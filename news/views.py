from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post
from .filters import PostFilter
from django.urls import reverse_lazy


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'all_posts'
    ordering = '-date_posted'
    paginate_by = 3

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_add.html'
    fields = ['title', 'text', 'author', 'post_category', 'post_type']
    permission_required = ('news.add_post', )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'text', 'post_category', 'post_type']
    permission_required = ('news.change_post', )



class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')
    permission_required = ('news.delete_post', )



class PostSearchView(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'all_posts'
    ordering = '-id'
    queryset = Post.objects.all()
    paginate_by = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }

