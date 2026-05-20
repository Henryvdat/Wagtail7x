import re
from django import template
from django.utils.safestring import mark_safe
from pathlib import Path
from django.contrib.staticfiles import finders
from wagtail.models import Site
from wagtail.rich_text import expand_db_html

register = template.Library()


@register.filter
def richtext_inline(value):
    """
    Like Wagtail's |richtext filter but strips the outer <div class="rich-text">
    wrapper, making it safe to use inside block-level elements like <h1> or <h2>.

    Usage:
        <h1>{{ page.rich_title|richtext_inline }}</h1>
    """
    if not value:
        return ''
    html = expand_db_html(value)
    # Remove the wrapping <div class="rich-text">...</div> that richtext adds
    html = re.sub(r'^<div[^>]*class="rich-text"[^>]*>(.*)</div>$', r'\1', html.strip(), flags=re.DOTALL)
    return mark_safe(html)


@register.simple_tag(takes_context=True)
def nav_pages(context):
    """Legacy tag — kept for backwards compatibility.
    The site now uses wagtailmenus {% main_menu %} instead."""
    request = context.get('request')
    if not request:
        return []
    site = Site.find_for_request(request)
    if not site:
        return []
    return site.root_page.get_children().live().in_menu()


@register.simple_tag
def heroicon(name, style='outline', css_class='', aria_hidden='true', title=''):
    """
    Render a Heroicon inline SVG.

    Usage:
        {% load nav_tags %}
        {% heroicon "arrow-right" %}
        {% heroicon "home" css_class="icon icon--sm" %}
        {% heroicon "magnifying-glass" aria_hidden="false" title="Search" %}

    Icons are loaded from mysite/static/mysite/icons/{style}/{name}.svg
    """
    relative_path = f'mysite/icons/{style}/{name}.svg'
    absolute_path = finders.find(relative_path)

    if not absolute_path:
        return mark_safe(f'<span class="icon-missing" title="Icon not found: {name}"></span>')

    svg_content = Path(absolute_path).read_text(encoding='utf-8').strip()

    attrs = []
    if css_class:
        attrs.append(f'class="{css_class}"')
    if aria_hidden:
        attrs.append(f'aria-hidden="{aria_hidden}"')

    if title:
        title_tag = f'<title>{title}</title>'
        close = svg_content.index('>') + 1
        svg_content = svg_content[:close] + title_tag + svg_content[close:]
        attrs = [a for a in attrs if 'aria-hidden' not in a]
        attrs.append('role="img"')

    if attrs:
        attr_string = ' '.join(attrs)
        svg_content = svg_content.replace('<svg ', f'<svg {attr_string} ', 1)

    return mark_safe(svg_content)
