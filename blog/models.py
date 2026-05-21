from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import TaggedItemBase

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string
from wagtail.images.models import Image

from home.blocks import STANDARD_BLOCKS


class BlogIndexPage(Page):

    # ── Card appearance ───────────────────────────────────────
    CARD_STYLE_CHOICES = [
        ("index_card",    "Index Card"),
        ("double_column", "Double-Column with Image"),
    ]
    card_style = models.CharField(
        max_length=32,
        choices=CARD_STYLE_CHOICES,
        default="index_card",
        verbose_name="Card style",
        help_text="Layout applied to every post card on this index page.",
    )
    card_image_bg_color = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name="Card image background colour",
        help_text="Any valid CSS colour (e.g. #f0e6d3, rgb(240,230,211), bisque). "
                  "Applied behind the thumbnail on the index listing only.",
    )

    # ── Header & subheader strip ─────────────────────────────
    header_bg_color = models.CharField(
        max_length=32,
        blank=True,
        default="",
        verbose_name="Header background colour",
        help_text="Overrides the nav bar background colour on this page. "
                  "Any valid CSS colour. Leave blank for the site default.",
    )
    subheader_bg_color = models.CharField(
        max_length=32,
        blank=True,
        default="#2d4a3e",
        verbose_name="Subheader background colour",
        help_text="Any valid CSS colour: hex (#1a2b3c), rgb(), named colour, etc.",
    )
    subheader_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Subheader image",
        help_text="Centred image displayed inside the coloured subheader strip.",
    )

    # ── Intro text (below the strip) ─────────────────────────
    subheader_text = RichTextField(
        blank=True,
        verbose_name="Intro text",
        help_text="Text displayed below the subheader strip, above the post listing.",
    )

    # ── Legacy fields ─────────────────────────────────────────
    intro = RichTextField(blank=True)
    body = StreamField(STANDARD_BLOCKS, use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("card_style"),
                FieldPanel("card_image_bg_color"),
            ],
            heading="Card appearance",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("header_bg_color"),
                FieldPanel("subheader_bg_color"),
                FieldPanel("subheader_image"),
            ],
            heading="Header & subheader strip",
            classname="collapsible",
        ),
        FieldPanel("subheader_text"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['blogpages'] = self.get_children().live().order_by('-first_published_at')
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = RichTextField(blank=True)
    body = StreamField(STANDARD_BLOCKS, use_json_field=True, blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # ── Header & subheader strip ─────────────────────────────
    header_bg_color = models.CharField(
        max_length=32,
        blank=True,
        default="",
        verbose_name="Header background colour",
        help_text="Overrides the nav bar background colour on this page. "
                  "Any valid CSS colour. Leave blank for the site default.",
    )
    subheader_bg_color = models.CharField(
        max_length=32,
        blank=True,
        default="",
        verbose_name="Subheader background colour",
        help_text="Any valid CSS colour. Leave blank to hide the subheader strip.",
    )
    subheader_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Subheader image",
        help_text="Centred image displayed inside the coloured subheader strip.",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("header_bg_color"),
                FieldPanel("subheader_bg_color"),
                FieldPanel("subheader_image"),
            ],
            heading="Header & subheader strip",
            classname="collapsible",
        ),
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("tags"),
        FieldPanel("main_image"),
    ]
