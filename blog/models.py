from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import TaggedItemBase

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import RichTextBlock, CharBlock, StructBlock, ChoiceBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    body = StreamField([
        ('rich_text', RichTextBlock(icon='pilcrow')),
        ('image', StructBlock([
            ('image', ImageChooserBlock()),
            ('caption', CharBlock(required=False)),
        ], template='home/blocks/image.html', icon='image')),
        ('section', StructBlock([
            ('heading', CharBlock()),
            ('body', RichTextBlock()),
            ('theme', ChoiceBlock(choices=[
                ('default', 'Default'),
                ('dark', 'Dark'),
                ('accent', 'Accent'),
            ], default='default')),
        ], template='home/blocks/section.html', icon='form')),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
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
    body = StreamField([
        ('rich_text', RichTextBlock(icon='pilcrow')),
        ('image', StructBlock([
            ('image', ImageChooserBlock()),
            ('caption', CharBlock(required=False)),
        ], template='home/blocks/image.html', icon='image')),
        ('quote', RichTextBlock(
            template='home/blocks/quote.html',
            icon='openquote',
        )),
        ('section', StructBlock([
            ('heading', CharBlock()),
            ('body', RichTextBlock()),
            ('theme', ChoiceBlock(choices=[
                ('default', 'Default'),
                ('dark', 'Dark'),
                ('accent', 'Accent'),
            ], default='default')),
        ], template='home/blocks/section.html', icon='form')),
    ], use_json_field=True, blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("tags"),
        FieldPanel("main_image"),
    ]