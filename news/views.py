from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from .models import Post
from .filters import PostFilter
from django.urls import reverse_lazy


class HomePageView(ListView):
    model = Post
    template_name = 'home.html'
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


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_add.html'
    fields = ['title', 'text', 'author', 'post_category', 'post_type']


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'text', 'post_category', 'post_type']


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


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

