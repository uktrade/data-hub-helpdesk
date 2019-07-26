from django import template

from wagtail.core.models import Page

register = template.Library()


@register.inclusion_tag('tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
            self, inclusive=True).filter(depth__gt=1)

    return {
        'ancestors': ancestors,
        'request': context['request'],
    }


@register.inclusion_tag('tags/author.html', takes_context=True)
def article_author(context):
    self = context.get('self')
    name = ''

    if self is None:
        name = 'Anon'
    else:
        name = f'{self.owner.first_name} {self.owner.last_name}'

    return {
        'name': name
    }
