"""
Trims card_style to two choices only:
  - index_card    → Index Card
  - double_column → Double-Column with Image

Removes the redundant double_column_fill option.
Note: Django stores choices as plain varchar; removing a choice from the
list does not require altering the column, only the field definition.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0020_blogindexpage_card_appearance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogindexpage",
            name="card_style",
            field=models.CharField(
                choices=[
                    ("index_card",    "Index Card"),
                    ("double_column", "Double-Column with Image"),
                ],
                default="index_card",
                help_text="Layout applied to every post card on this index page.",
                max_length=32,
                verbose_name="Card style",
            ),
        ),
    ]
