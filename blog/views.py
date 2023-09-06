from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from blog.models import Article
from blog.forms import ArticleForm
from django.urls import reverse_lazy, reverse
from blog.services import get_articles_cache


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    permission_required = 'blog.add_article'
    success_url = reverse_lazy('blog:list')


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    permission_required = 'blog.change_article'

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class ArticleListView(ListView):
    model = Article

    def get_context_data(self, **kwargs):
        context = {
            'object_list': get_articles_cache()
        }
        return context


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

