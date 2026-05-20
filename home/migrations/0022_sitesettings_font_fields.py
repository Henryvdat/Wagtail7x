from django.db import migrations, models

FONT_STACK_CHOICES = [
    ("", "— CSS default —"),
    ("system_sans",    "System UI (modern sans-serif)"),
    ("helvetica",      "Helvetica / Arial (neutral sans-serif)"),
    ("optima",         "Optima / Candara (humanist sans-serif)"),
    ("gill_sans",      "Gill Sans (humanist sans-serif)"),
    ("trebuchet",      "Trebuchet MS (friendly sans-serif)"),
    ("century_gothic", "Century Gothic / Futura (geometric sans-serif)"),
    ("georgia",        "Georgia (classic serif)"),
    ("palatino",       "Palatino (elegant serif)"),
    ("baskerville",    "Baskerville (transitional serif)"),
    ("garamond",       "Garamond (old-style serif)"),
    ("courier",        "Courier New (monospace)"),
]


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_sitesettings_font_pair'),
    ]

    operations = [
        # Remove the old combined font_pair field
        migrations.RemoveField(
            model_name='sitesettings',
            name='font_pair',
        ),
        # Add three independent font fields
        migrations.AddField(
            model_name='sitesettings',
            name='font_header',
            field=models.CharField(
                blank=True,
                choices=FONT_STACK_CHOICES,
                default='',
                help_text='Font for the navigation bar and logo. Leave blank for the CSS default.',
                max_length=64,
                verbose_name='Site header font',
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='font_heading',
            field=models.CharField(
                blank=True,
                choices=FONT_STACK_CHOICES,
                default='',
                help_text='Applied universally to all headings and page titles across the site. Leave blank for the CSS default.',
                max_length=64,
                verbose_name='Heading font (h1–h6 + page titles)',
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='font_body',
            field=models.CharField(
                blank=True,
                choices=FONT_STACK_CHOICES,
                default='',
                help_text='Font for all paragraph and general page text. Leave blank for the CSS default.',
                max_length=64,
                verbose_name='Body text font',
            ),
        ),
    ]
