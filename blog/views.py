from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from blog.models import Article
from django.urls import reverse_lazy, reverse


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'content', 'preview', 'creation_date')
    permission_required = 'blog.add_article'
    success_url = reverse_lazy('blog:list')


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'content', 'preview')
    permission_required = 'blog.change_article'

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class ArticleListView(ListView):
    model = Article


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Article
    permission_required = 'blog.delete_article'
    success_url = reverse_lazy('blog:list')

