from django.db import models

from wagtail.core.models import Page

from article.models import (
    ArticlePage,
    ArticleIndexPage,
)


class HomePage(Page):

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)

        recent = ArticlePage.objects.live().descendant_of(self).not_type(ArticleIndexPage).order_by('-date')
        child_categories = ArticleIndexPage.objects.live().child_of(self).order_by('title')

        context['recent'] = recent
        context['child_categories'] = child_categories

        return context
