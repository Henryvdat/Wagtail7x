import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0017_sitesettings_header_fields"),
        ("wagtailimages", "0027_image_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="standardpage",
            name="subheader_bg_color",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Any valid CSS colour: hex (#1a2b3c), rgb(), named colour, etc. "
                          "Leave blank to hide the subheader strip.",
                max_length=32,
                verbose_name="Subheader background colour",
            ),
        ),
        migrations.AddField(
            model_name="standardpage",
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
    ]
