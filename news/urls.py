from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostSearchView,
    subscribe,
    unsubscribe,
    CategoryListView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('add/', PostCreateView.as_view(), name='post_add'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('all_categories/', CategoryListView.as_view(), name='all_categories'),
    path('all_categories/subscribe/<int:pk>', subscribe),
    path('all_categories/unsubscribe/<int:pk>', unsubscribe),
]