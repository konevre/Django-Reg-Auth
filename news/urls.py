from django.urls import path
from .views import (
    HomePageView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostSearchView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/add/', PostCreateView.as_view(), name='post_add'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('search/', PostSearchView.as_view(), name='post_search')
]