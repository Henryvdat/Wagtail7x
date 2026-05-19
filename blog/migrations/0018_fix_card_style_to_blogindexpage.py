"""
Database-only fix: move card_style column from blog_blogpage to blog_blogindexpage.

The migration state is already correct after 0017 (card_style lives on
blogindexpage in the state). What's wrong is the physical database:

  - blog_blogpage may have a card_style column (from the original 0017)
  - blog_blogindexpage is missing the card_style column entirely

This migration fixes only the database to match the state — no state
operations are needed.
"""
from django.db import migrations


def fix_card_style_columns(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:

        # 1. Drop card_style from blog_blogpage if it was added by the original 0017
        cursor.execute("PRAGMA table_info(blog_blogpage)")
        if 'card_style' in [row[1] for row in cursor.fetchall()]:
            cursor.execute("ALTER TABLE blog_blogpage DROP COLUMN card_style")

        # 2. Add card_style to blog_blogindexpage if it is missing
        cursor.execute("PRAGMA table_info(blog_blogindexpage)")
        if 'card_style' not in [row[1] for row in cursor.fetchall()]:
            cursor.execute(
                "ALTER TABLE blog_blogindexpage "
                "ADD COLUMN card_style varchar(20) NOT NULL DEFAULT 'classic'"
            )


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_blogpage_card_style'),
    ]

    operations = [
        # SeparateDatabaseAndState with empty state_operations lets us run
        # raw SQL to fix the database without touching the migration state
        # (which 0017 already set correctly).
        migrations.SeparateDatabaseAndState(
            state_operations=[],
            database_operations=[
                migrations.RunPython(
                    fix_card_style_columns,
                    migrations.RunPython.noop,
                ),
            ],
        ),
    ]
