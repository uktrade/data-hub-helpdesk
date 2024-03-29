from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from wagtail.search import index


class ArticleIndexPage(Page):
    intro = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(ArticleIndexPage, self).get_context(request, *args, **kwargs)

        children = ArticlePage.objects.live().child_of(self).not_type(ArticleIndexPage).order_by('-date')
        siblings = ArticleIndexPage.objects.live().sibling_of(self).order_by('title')

        child_groups = ArticleIndexPage.objects.live().child_of(self).type(ArticleIndexPage).order_by('title')

        child_groups_for_layout = []
        row = []
        offset = 0
        for group in child_groups:
            row.append(group)

            offset += 1
            if offset % 3 == 0:
                child_groups_for_layout.append(row)
                row = []

        child_groups_for_layout.append(row)

        context['children'] = children
        context['siblings'] = siblings
        context['child_groups'] = child_groups_for_layout

        return context


class ArticlePage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250, blank=True, null=True)
    # body = RichTextField(blank=True)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(ArticlePage, self).get_context(request, *args, **kwargs)

        context['siblings'] = ArticlePage.objects.live().sibling_of(self, inclusive=False).order_by('title')

        return context
