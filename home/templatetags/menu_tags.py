from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def nav_pages(context):
    request = context.get('request')
    if not request or not hasattr(request, 'site') or not request.site:
        return []
    return request.site.root_page.get_children().live().in_menu()
