from django.urls import path

from blog.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('edit/<int:pk>', ArticleUpdateView.as_view(), name='edit'),
    path('view/<int:pk>', ArticleDetailView.as_view(), name='view'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('delete/<int:pk>', ArticleDeleteView.as_view(), name='delete'),
]
