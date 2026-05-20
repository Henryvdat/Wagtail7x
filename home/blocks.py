from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.images.blocks import ImageChooserBlock

ALIGNMENT_CHOICES = [
    ('left',   'Left'),
    ('center', 'Center'),
    ('right',  'Right'),
    ('full',   'Full width'),
]


class BlockStylesBlock(StructBlock):
    """
    Reusable style options embedded in every block.
    Renders as a collapsible group at the bottom of each block in the admin.
    """
    card         = BooleanBlock(required=False, label='Card style',
                                help_text='White background, rounded corners, drop shadow')
    background   = CharBlock(required=False, label='Background colour',
                             help_text='Any CSS colour — e.g. #f0f4ff, tomato, rgba(0,0,0,0.05)')
    text_color   = CharBlock(required=False, label='Text colour',
                             help_text='Any CSS colour — e.g. white, #333, rgba(0,0,0,0.8)')
    border       = BooleanBlock(required=False, label='Add border')
    border_color = CharBlock(required=False, label='Border colour',
                             help_text='Leave blank for default grey — e.g. #e07b39')
    custom_classes = CharBlock(required=False, label='Extra CSS classes',
                               help_text='Class names defined in your CSS files, without the dot — e.g. "highlight" for .highlight { }. Define custom classes in mysite/static/mysite/css/. Multiple classes: "highlight bold-text"')

    class Meta:
        icon  = 'cog'
        label = 'Block styles'
        form_classname = 'block-styles-struct'


class RichTextAlignedBlock(StructBlock):
    alignment = ChoiceBlock(choices=ALIGNMENT_CHOICES, default='full', required=False)
    content   = RichTextBlock()
    styles    = BlockStylesBlock(required=False, label='Block styles')

    class Meta:
        template = 'home/blocks/rich_text.html'
        icon = 'pilcrow'
        label = 'Rich Text'


class ImageAlignedBlock(StructBlock):
    image     = ImageChooserBlock()
    caption   = CharBlock(required=False)
    alignment = ChoiceBlock(choices=ALIGNMENT_CHOICES, default='full', required=False)
    styles    = BlockStylesBlock(required=False, label='Block styles')

    class Meta:
        template = 'home/blocks/image.html'
        icon = 'image'
        label = 'Image'


class ThumbnailAlignedBlock(StructBlock):
    image     = ImageChooserBlock()
    caption   = CharBlock(required=False)
    alignment = ChoiceBlock(choices=ALIGNMENT_CHOICES, default='left', required=False)
    styles    = BlockStylesBlock(required=False, label='Block styles')

    class Meta:
        template = 'home/blocks/thumbnail.html'
        icon = 'image'
        label = 'Thumbnail'


class QuoteAlignedBlock(StructBlock):
    content   = RichTextBlock()
    alignment = ChoiceBlock(choices=ALIGNMENT_CHOICES, default='center', required=False)
    styles    = BlockStylesBlock(required=False, label='Block styles')

    class Meta:
        template = 'home/blocks/quote.html'
        icon = 'openquote'
        label = 'Quote'


class SectionBlock(StructBlock):
    heading   = CharBlock()
    body      = RichTextBlock()
    theme     = ChoiceBlock(choices=[
        ('default', 'Default'),
        ('dark',    'Dark'),
        ('accent',  'Accent'),
    ], default='default')
    alignment = ChoiceBlock(choices=ALIGNMENT_CHOICES, default='full', required=False)
    styles    = BlockStylesBlock(required=False, label='Block styles')

    class Meta:
        template = 'home/blocks/section.html'
        icon = 'form'
        label = 'Section'


class StyledTableBlock(StructBlock):
    """
    TypedTableBlock wrapped with a caption, alignment, and shared BlockStylesBlock options.
    Columns are typed (text, rich_text, numeric) and defined by the editor at authoring time.
    """
    caption = CharBlock(
        required=False,
        label='Caption',
        help_text='Optional table caption — recommended for accessibility.',
    )
    table = TypedTableBlock([
        ('text',      CharBlock()),
        ('rich_text', RichTextBlock()),
        ('numeric',   CharBlock(
            help_text='Enter a number. Right-aligned in the rendered table.',
        )),
    ], label='Table data')
    header_bg_color   = CharBlock(required=False, label='Header background colour',
                                  help_text='Any CSS colour — e.g. #1a2b3c, steelblue. Leave blank for no background.')
    header_text_color = CharBlock(required=False, label='Header text colour',
                                  help_text='Any CSS colour — e.g. white, #333. Leave blank for default.')
    alignment = ChoiceBlock(choices=ALIGNMENT_CHOICES, default='full', required=False)
    striped    = BooleanBlock(required=False, label='Striped rows',
                              help_text='Alternate row background colour for readability.')
    styles     = BlockStylesBlock(required=False, label='Block styles')

    class Meta:
        template = 'home/blocks/table.html'
        icon  = 'table'
        label = 'Table'


# Blocks available inside columns (no nesting columns within columns)
class ColumnContentBlock(StreamBlock):
    rich_text = RichTextAlignedBlock()
    image     = ImageAlignedBlock()
    thumbnail = ThumbnailAlignedBlock()
    quote     = QuoteAlignedBlock()
    table     = StyledTableBlock()
    raw_html  = RawHTMLBlock(label='Raw HTML', icon='code')

    class Meta:
        icon = 'placeholder'


class TwoColumnBlock(StructBlock):
    layout = ChoiceBlock(choices=[
        ('1-1', '50% / 50%'),
        ('2-1', '66% / 33%'),
        ('1-2', '33% / 66%'),
    ], default='1-1', label='Column ratio')
    left   = ColumnContentBlock()
    right  = ColumnContentBlock()
    styles = BlockStylesBlock(required=False, label='Block styles')

    class Meta:
        template = 'home/blocks/two_column.html'
        icon = 'grip'
        label = 'Two Columns'


class ThreeColumnBlock(StructBlock):
    left   = ColumnContentBlock()
    center = ColumnContentBlock()
    right  = ColumnContentBlock()
    styles = BlockStylesBlock(required=False, label='Block styles')

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
    ('table',        StyledTableBlock()),
    ('section',      SectionBlock()),
    ('two_columns',  TwoColumnBlock()),
    ('three_columns', ThreeColumnBlock()),
    ('raw_html',     RawHTMLBlock(label='Raw HTML', icon='code')),
]
