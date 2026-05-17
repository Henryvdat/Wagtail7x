from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.images import get_image_model_string
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from .blocks import STANDARD_BLOCKS


class HomePage(Page):
    intro = RichTextField(blank=True)
    body = StreamField(STANDARD_BLOCKS, use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    template = 'home/home_page.html'


class StandardPage(Page):
    intro = RichTextField(blank=True)
    body = StreamField(STANDARD_BLOCKS, use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    template = 'home/standard_page.html'


@register_setting
class SiteSettings(BaseSiteSetting):
    header_icon = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name="Header icon")
    footer_text = RichTextField(blank=True, default="Neil Whittaker. Built with Wagtail.", verbose_name="Footer text")
    panels = [FieldPanel("header_icon"), FieldPanel("footer_text")]

    class Meta:
        verbose_name = "Site Settings"
