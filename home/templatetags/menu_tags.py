from django import template
from wagtail.models import Site

register = template.Library()

@register.simple_tag(takes_context=True)
def nav_pages(context):
    request = context.get('request')
    if not request:
        return []
    site = Site.find_for_request(request)
    if not site:
        return []
    return site.root_page.get_children().live().in_menu()
