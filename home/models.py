from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.images import get_image_model_string
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from .blocks import STANDARD_BLOCKS


class HomePage(Page):
    intro = RichTextField(blank=True)
    body = StreamField(STANDARD_BLOCKS, use_json_field=True, blank=True)
    title_css_classes = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Title CSS classes",
        help_text="Space-separated CSS classes to apply to the page title <h1>, e.g. 'text-hero text-center u-color-accent'",
    )

    content_panels = Page.content_panels + [
        FieldPanel('title_css_classes'),
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
    # ── Header ───────────────────────────────────────────────
    site_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Site name",
        help_text="Overrides the Wagtail site name shown in the header. Leave blank to use the default.",
    )
    site_name_css_classes = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Site name CSS classes",
        help_text="Space-separated CSS classes on the site name text, e.g. 'text-xl font-bold u-color-accent'",
    )
    header_icon = models.ForeignKey(
        get_image_model_string(), null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
        verbose_name="Header icon",
    )
    header_icon_css_classes = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Header icon CSS classes",
        help_text="Space-separated CSS classes on the header icon image, e.g. 'rounded-full'",
    )

    # ── Footer ───────────────────────────────────────────────
    footer_text = RichTextField(
        blank=True,
        default="Neil Whittaker. Built with Wagtail.",
        verbose_name="Footer text",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("site_name"),
                FieldPanel("site_name_css_classes"),
                FieldPanel("header_icon"),
                FieldPanel("header_icon_css_classes"),
            ],
            heading="Header",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("footer_text"),
            ],
            heading="Footer",
            classname="collapsible",
        ),
    ]

    class Meta:
        verbose_name = "Site Settings"
