from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_alter_blogindexpage_subheader_bg_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogindexpage',
            name='header_bg_color',
        ),
        migrations.RemoveField(
            model_name='blogindexpage',
            name='subheader_bg_color',
        ),
        migrations.RemoveField(
            model_name='blogindexpage',
            name='subheader_image',
        ),
    ]
