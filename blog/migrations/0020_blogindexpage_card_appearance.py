"""
Updates BlogIndexPage card appearance fields:
  - Alters card_style: new named choices, max_length 32, default 'index_card'
  - Adds card_image_bg_color: optional CSS colour for the thumbnail background
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0019_merge_20260519_1504"),
    ]

    operations = [
        # Update card_style to new choices / default
        migrations.AlterField(
            model_name="blogindexpage",
            name="card_style",
            field=models.CharField(
                choices=[
                    ("index_card",         "Index Card"),
                    ("double_column",      "Double-Column with Image"),
                    ("double_column_fill", "Double-Column with Image (Full Height)"),
                ],
                default="index_card",
                help_text="Layout applied to every post card on this index page.",
                max_length=32,
                verbose_name="Card style",
            ),
        ),
        # Add new card_image_bg_color field
        migrations.AddField(
            model_name="blogindexpage",
            name="card_image_bg_color",
            field=models.CharField(
                blank=True,
                default="",
                help_text=(
                    "Any valid CSS colour (e.g. #f0e6d3, rgb(240,230,211), bisque). "
                    "Applied behind the thumbnail on the index listing only."
                ),
                max_length=64,
                verbose_name="Card image background colour",
            ),
        ),
    ]
