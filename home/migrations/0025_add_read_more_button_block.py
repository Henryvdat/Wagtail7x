# Hand-crafted migration — adds ReadMoreButtonBlock to STANDARD_BLOCKS and ColumnContentBlock
# for HomePage and StandardPage body StreamFields.

import wagtail.fields
from django.db import migrations

BLOCK_LOOKUP = {
    0:  ('wagtail.blocks.ChoiceBlock', [], {'choices': [('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('full', 'Full width')], 'required': False}),
    1:  ('wagtail.blocks.RichTextBlock', (), {}),
    2:  ('wagtail.blocks.BooleanBlock', (), {'help_text': 'White background, rounded corners, drop shadow', 'label': 'Card style', 'required': False}),
    3:  ('wagtail.blocks.CharBlock', (), {'help_text': 'Any CSS colour — e.g. #f0f4ff, tomato, rgba(0,0,0,0.05)', 'label': 'Background colour', 'required': False}),
    4:  ('wagtail.blocks.CharBlock', (), {'help_text': 'Any CSS colour — e.g. white, #333, rgba(0,0,0,0.8)', 'label': 'Text colour', 'required': False}),
    5:  ('wagtail.blocks.BooleanBlock', (), {'label': 'Add border', 'required': False}),
    6:  ('wagtail.blocks.CharBlock', (), {'help_text': 'Leave blank for default grey — e.g. #e07b39', 'label': 'Border colour', 'required': False}),
    7:  ('wagtail.blocks.CharBlock', (), {'help_text': 'Class names defined in your CSS files, without the dot — e.g. "highlight" for .highlight { }. Define custom classes in mysite/static/mysite/css/. Multiple classes: "highlight bold-text"', 'label': 'Extra CSS classes', 'required': False}),
    8:  ('wagtail.blocks.StructBlock', [[('card', 2), ('background', 3), ('text_color', 4), ('border', 5), ('border_color', 6), ('custom_classes', 7)]], {'label': 'Block styles', 'required': False}),
    9:  ('wagtail.blocks.StructBlock', [[('alignment', 0), ('content', 1), ('styles', 8)]], {}),
    10: ('wagtail.images.blocks.ImageChooserBlock', (), {}),
    11: ('wagtail.blocks.CharBlock', (), {'required': False}),
    12: ('wagtail.blocks.StructBlock', [[('image', 10), ('caption', 11), ('alignment', 0), ('styles', 8)]], {}),
    13: ('wagtail.blocks.StructBlock', [[('content', 1), ('alignment', 0), ('styles', 8)]], {}),
    14: ('wagtail.blocks.CharBlock', (), {'help_text': 'Optional table caption — recommended for accessibility.', 'label': 'Caption', 'required': False}),
    15: ('wagtail.blocks.CharBlock', (), {}),
    16: ('wagtail.blocks.CharBlock', (), {'help_text': 'Enter a number. Right-aligned in the rendered table.'}),
    17: ('wagtail.contrib.typed_table_block.blocks.TypedTableBlock', [[('text', 15), ('rich_text', 1), ('numeric', 16)]], {'label': 'Table data'}),
    18: ('wagtail.blocks.CharBlock', (), {'help_text': 'Any CSS colour — e.g. #1a2b3c, steelblue. Leave blank for no background.', 'label': 'Header background colour', 'required': False}),
    19: ('wagtail.blocks.CharBlock', (), {'help_text': 'Any CSS colour — e.g. white, #333. Leave blank for default.', 'label': 'Header text colour', 'required': False}),
    20: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'Alternate row background colour for readability.', 'label': 'Striped rows', 'required': False}),
    21: ('wagtail.blocks.StructBlock', [[('caption', 14), ('table', 17), ('header_bg_color', 18), ('header_text_color', 19), ('alignment', 0), ('striped', 20), ('styles', 8)]], {}),
    22: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('default', 'Default'), ('dark', 'Dark'), ('accent', 'Accent')]}),
    23: ('wagtail.blocks.StructBlock', [[('heading', 15), ('body', 1), ('theme', 22), ('alignment', 0), ('styles', 8)]], {}),
    24: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('1-1', '50% / 50%'), ('2-1', '66% / 33%'), ('1-2', '33% / 66%')], 'label': 'Column ratio'}),
    25: ('wagtail.blocks.RawHTMLBlock', (), {'icon': 'code', 'label': 'Raw HTML'}),
    # 26 updated: ColumnContentBlock now includes read_more_button (32)
    26: ('wagtail.blocks.StreamBlock', [[('rich_text', 9), ('image', 12), ('thumbnail', 12), ('quote', 13), ('table', 21), ('read_more_button', 32), ('raw_html', 25)]], {}),
    27: ('wagtail.blocks.StructBlock', [[('layout', 24), ('left', 26), ('right', 26), ('styles', 8)]], {}),
    28: ('wagtail.blocks.StructBlock', [[('left', 26), ('center', 26), ('right', 26), ('styles', 8)]], {}),
    # New entries for ReadMoreButtonBlock
    29: ('wagtail.blocks.PageChooserBlock', (), {'help_text': 'The page this button links to.', 'label': 'Target page'}),
    30: ('wagtail.blocks.CharBlock', (), {'default': 'Read more', 'help_text': 'Label displayed on the button.', 'label': 'Button text', 'max_length': 100}),
    31: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('solid', 'Solid (filled)'), ('outline', 'Outline'), ('ghost', 'Ghost (text only)')], 'default': 'solid', 'label': 'Button style'}),
    32: ('wagtail.blocks.StructBlock', [[('button_text', 30), ('page', 29), ('button_style', 31), ('alignment', 0), ('styles', 8)]], {}),
}

TOP_LEVEL = [
    ('rich_text', 9), ('image', 12), ('thumbnail', 12), ('quote', 13),
    ('table', 21), ('section', 23), ('read_more_button', 32),
    ('two_columns', 27), ('three_columns', 28), ('raw_html', 25),
]


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_homepage_header_bg_color_homepage_subheader_bg_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField(TOP_LEVEL, blank=True, block_lookup=BLOCK_LOOKUP),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='body',
            field=wagtail.fields.StreamField(TOP_LEVEL, blank=True, block_lookup=BLOCK_LOOKUP),
        ),
    ]
