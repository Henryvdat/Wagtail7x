from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_remove_standardpage_rich_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='font_pair',
            field=models.CharField(
                blank=True,
                choices=[
                    ('poppins_inter',       'Poppins + Inter (default)'),
                    ('playfair_lato',       'Playfair Display + Lato'),
                    ('montserrat_opensans', 'Montserrat + Open Sans'),
                    ('merriweather_source', 'Merriweather + Source Sans 3'),
                    ('raleway_nunito',      'Raleway + Nunito'),
                    ('oswald_pt',           'Oswald + PT Sans'),
                    ('lora_inter',          'Lora + Inter'),
                    ('dm_serif_dm_sans',    'DM Serif Display + DM Sans'),
                ],
                default='',
                help_text='Choose a heading + body font combination. Leave blank to use the CSS default (Poppins + Inter).',
                max_length=64,
                verbose_name='Font pair',
            ),
        ),
    ]
