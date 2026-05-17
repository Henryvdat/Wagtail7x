from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.blocks import (
    RichTextBlock,
    CharBlock,
    StructBlock,
    ChoiceBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images import get_image_model_string
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


class HomePage(Page):
    intro = models.TextField(blank=True)

    body = StreamField([

        ('rich_text', RichTextBlock(
            icon='pilcrow',
        )),

        # Full-width image — renders at max 1200x900, aspect ratio preserved
        ('image', StructBlock([
            ('image',   ImageChooserBlock()),
            ('caption', CharBlock(required=False)),
        ], template='home/blocks/image.html', icon='image')),

        # Thumbnail image — renders at a fixed 200x200, centre-cropped
        ('thumbnail', StructBlock([
            ('image',   ImageChooserBlock()),
            ('caption', CharBlock(required=False)),
        ], template='home/blocks/thumbnail.html', icon='image')),

        ('quote', RichTextBlock(
            template='home/blocks/quote.html',
            icon='openquote',
        )),

        ('section', StructBlock([
            ('heading', CharBlock()),
            ('body',    RichTextBlock()),
            ('theme',   ChoiceBlock(choices=[
                ('default', 'Default'),
                ('dark',    'Dark'),
                ('accent',  'Accent'),
            ], default='default')),
        ], template='home/blocks/section.html', icon='form')),

    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    template = 'home/home_page.html'

@register_setting
class SiteSettings(BaseSiteSetting):
    header_icon = models.ForeignKey(get_image_model_string(),null=True,blank=True,on_delete=models.SET_NULL,related_name="+",verbose_name="Header icon")
    footer_text = RichTextField(blank=True, default="Neil Whittaker. Built with Wagtail.", verbose_name="Footer text")
    panels=[FieldPanel("header_icon"),FieldPanel("footer_text")]
    class Meta:
        verbose_name="Site Settings"
