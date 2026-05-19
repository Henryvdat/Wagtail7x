import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0016_alter_blogindexpage_body_alter_blogpage_body"),
        ("wagtailimages", "0027_image_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogindexpage",
            name="subheader_bg_color",
            field=models.CharField(
                blank=True,
                default="#2d4a3e",
                help_text="Any valid CSS colour: hex (#1a2b3c), rgb(), named colour, etc.",
                max_length=32,
                verbose_name="Subheader background colour",
            ),
        ),
        migrations.AddField(
            model_name="blogindexpage",
            name="subheader_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Centred image displayed inside the coloured subheader strip.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
                verbose_name="Subheader image",
            ),
        ),
        migrations.AddField(
            model_name="blogindexpage",
            name="subheader_text",
            field=wagtail.fields.RichTextField(
                blank=True,
                help_text="Text displayed below the subheader strip, above the post listing.",
                verbose_name="Intro text",
            ),
        ),
    ]
