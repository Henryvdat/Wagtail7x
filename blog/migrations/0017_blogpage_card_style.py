"""
Schema migration: add card_style field to BlogIndexPage.

Controls the card layout used for all blog post cards on the listing page.
The dropdown appears when editing the Blog Index Page in the Wagtail admin.

Choices:
  'classic'     — existing stacked layout (image / title / intro / link)
  'two_column'  — new layout with text on the left, image on the right
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_alter_blogindexpage_body_alter_blogpage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogindexpage',
            name='card_style',
            field=models.CharField(
                choices=[
                    ('classic',    'Classic — stacked image / title / intro / link'),
                    ('two_column', 'Two-column — text left, image right'),
                ],
                default='classic',
                help_text='Layout used for all post cards on this blog listing page.',
                max_length=20,
                verbose_name='Card style',
            ),
        ),
    ]
