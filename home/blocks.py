from wagtail.blocks import (
    RichTextBlock,
    CharBlock,
    StructBlock,
    ChoiceBlock,
    StreamBlock,
)
from wagtail.images.blocks import ImageChooserBlock

ALIGNMENT_CHOICES = [
    ('left',   'Left'),
    ('center', 'Center'),
    ('right',  'Right'),
    ('full',   'Full width'),
]


class RichTextAlignedBlock(StructBlock):
    alignment = ChoiceBlock(choices=ALIGNMENT_CHOICES, default='full', required=False)
    content = RichTextBlock()

    class Meta:
        template = 'home/blocks/rich_text.html'
        icon = 'pilcrow'
        label = 'Rich Text'


class ImageAlignedBlock(StructBlock):
    image = ImageChooserBlock()
    caption = CharBlock(required=False)
    alignment = ChoiceBlock(choices=ALIGNMENT_CHOICES, default='full', required=False)

    class Meta:
        template = 'home/blocks/image.html'
        icon = 'image'
        label = 'Image'


class ThumbnailAlignedBlock(StructBlock):
    image = ImageChooserBlock()
    caption = CharBlock(required=False)
    alignment = ChoiceBlock(choices=ALIGNMENT_CHOICES, default='left', required=False)

    class Meta:
        template = 'home/blocks/thumbnail.html'
        icon = 'image'
        label = 'Thumbnail'


class QuoteAlignedBlock(StructBlock):
    content = RichTextBlock()
    alignment = ChoiceBlock(choices=ALIGNMENT_CHOICES, default='center', required=False)

    class Meta:
        template = 'home/blocks/quote.html'
        icon = 'openquote'
        label = 'Quote'


class SectionBlock(StructBlock):
    heading = CharBlock()
    body = RichTextBlock()
    theme = ChoiceBlock(choices=[
        ('default', 'Default'),
        ('dark',    'Dark'),
        ('accent',  'Accent'),
    ], default='default')
    alignment = ChoiceBlock(choices=ALIGNMENT_CHOICES, default='full', required=False)

    class Meta:
        template = 'home/blocks/section.html'
        icon = 'form'
        label = 'Section'


# Blocks available inside columns (no nesting columns within columns)
class ColumnContentBlock(StreamBlock):
    rich_text = RichTextAlignedBlock()
    image = ImageAlignedBlock()
    thumbnail = ThumbnailAlignedBlock()
    quote = QuoteAlignedBlock()

    class Meta:
        icon = 'placeholder'


class TwoColumnBlock(StructBlock):
    layout = ChoiceBlock(choices=[
        ('1-1', '50% / 50%'),
        ('2-1', '66% / 33%'),
        ('1-2', '33% / 66%'),
    ], default='1-1', label='Column ratio')
    left = ColumnContentBlock()
    right = ColumnContentBlock()

    class Meta:
        template = 'home/blocks/two_column.html'
        icon = 'grip'
        label = 'Two Columns'


class ThreeColumnBlock(StructBlock):
    left = ColumnContentBlock()
    center = ColumnContentBlock()
    right = ColumnContentBlock()

    class Meta:
        template = 'home/blocks/three_column.html'
        icon = 'grip'
        label = 'Three Columns'


# Shared block list used across all page types
STANDARD_BLOCKS = [
    ('rich_text',    RichTextAlignedBlock()),
    ('image',        ImageAlignedBlock()),
    ('thumbnail',    ThumbnailAlignedBlock()),
    ('quote',        QuoteAlignedBlock()),
    ('section',      SectionBlock()),
    ('two_columns',  TwoColumnBlock()),
    ('three_columns', ThreeColumnBlock()),
]
