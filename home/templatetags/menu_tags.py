# home/templatetags/menu_tags.py
#
# This file exists only to silence Django's W003 warning about duplicate
# templatetag module names.  It re-exports the wagtailmenus register so that
# {% load menu_tags %} in any template gets full access to wagtailmenus tags
# (main_menu, flat_menu, etc.) even though `home` is listed before
# `wagtailmenus` in INSTALLED_APPS.
from wagtailmenus.templatetags.menu_tags import register  # noqa: F401
