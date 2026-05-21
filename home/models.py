from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.images import get_image_model_string
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from .blocks import STANDARD_BLOCKS


# ── Font stack catalogue — system / local fonts only, no external loading ────
#
# Each value is a CSS font-family stack that works without any network request.
# The key is stored in the DB; base.html injects the value as a CSS variable.
#
# Three fields use this catalogue independently:
#   font_header  → --font-header  (site nav bar)
#   font_heading → --font-heading (all h1–h6, page titles, universally)
#   font_body    → --font-body    (body / paragraph text)

FONT_STACKS = {
    "system_sans": {
        "label": "System UI (modern sans-serif)",
        "stack": "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
    },
    "helvetica": {
        "label": "Helvetica / Arial (neutral sans-serif)",
        "stack": "'Helvetica Neue', Helvetica, Arial, sans-serif",
    },
    "optima": {
        "label": "Optima / Candara (humanist sans-serif)",
        "stack": "Optima, Candara, 'Gill Sans', Calibri, sans-serif",
    },
    "gill_sans": {
        "label": "Gill Sans (humanist sans-serif)",
        "stack": "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    },
    "trebuchet": {
        "label": "Trebuchet MS (friendly sans-serif)",
        "stack": "'Trebuchet MS', 'Lucida Grande', Tahoma, sans-serif",
    },
    "century_gothic": {
        "label": "Century Gothic / Futura (geometric sans-serif)",
        "stack": "'Century Gothic', Futura, 'Gill Sans', sans-serif",
    },
    "georgia": {
        "label": "Georgia (classic serif)",
        "stack": "Georgia, 'Times New Roman', serif",
    },
    "palatino": {
        "label": "Palatino (elegant serif)",
        "stack": "Palatino, 'Palatino Linotype', 'Book Antiqua', Georgia, serif",
    },
    "baskerville": {
        "label": "Baskerville (transitional serif)",
        "stack": "Baskerville, 'Baskerville Old Face', 'Hoefler Text', Garamond, serif",
    },
    "garamond": {
        "label": "Garamond (old-style serif)",
        "stack": "Garamond, Baskerville, 'Book Antiqua', serif",
    },
    "courier": {
        "label": "Courier New (monospace)",
        "stack": "'Courier New', Courier, monospace",
    },
}

FONT_STACK_CHOICES = [("", "— CSS default —")] + [
    (k, v["label"]) for k, v in FONT_STACKS.items()
]


class HomePage(Page):
    rich_title = RichTextField(
        blank=True,
        features=['bold', 'italic', 'link', 'superscript', 'subscript'],
        verbose_name="Display title (rich text)",
        help_text="Optional. Replaces the plain title on the page. "
                  "Supports bold, italic, links. Leave blank to use the plain title above.",
    )
    intro = RichTextField(blank=True)
    body = StreamField(STANDARD_BLOCKS, use_json_field=True, blank=True)
    title_css_classes = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Title CSS classes",
        help_text="Space-separated CSS classes to apply to the page title <h1>, e.g. 'text-hero text-center u-color-accent'",
    )

    # ── Header & subheader ───────────────────────────────────
    header_bg_color = models.CharField(
        max_length=32,
        blank=True,
        default="",
        verbose_name="Header background colour",
        help_text="Overrides the nav bar background colour on this page. "
                  "Any valid CSS colour (e.g. #1a3a5c, darkgreen). Leave blank for the site default.",
    )
    subheader_bg_color = models.CharField(
        max_length=32,
        blank=True,
        default="",
        verbose_name="Subheader background colour",
        help_text="Any valid CSS colour. Leave blank to hide the subheader strip.",
    )
    subheader_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Subheader image",
        help_text="Centred image displayed inside the coloured subheader strip.",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("header_bg_color"),
                FieldPanel("subheader_bg_color"),
                FieldPanel("subheader_image"),
            ],
            heading="Header & subheader",
            classname="collapsible",
        ),
        FieldPanel('rich_title'),
        FieldPanel('title_css_classes'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    template = 'home/home_page.html'


class StandardPage(Page):
    # ── Header & subheader strip ─────────────────────────────
    header_bg_color = models.CharField(
        max_length=32,
        blank=True,
        default="",
        verbose_name="Header background colour",
        help_text="Overrides the nav bar background colour on this page. "
                  "Any valid CSS colour (e.g. #1a3a5c, darkgreen). Leave blank for the site default.",
    )
    subheader_bg_color = models.CharField(
        max_length=32,
        blank=True,
        default="",
        verbose_name="Subheader background colour",
        help_text="Any valid CSS colour: hex (#1a2b3c), rgb(), named colour, etc. "
                  "Leave blank to hide the subheader strip.",
    )
    subheader_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Subheader image",
        help_text="Centred image displayed inside the coloured subheader strip.",
    )

    intro = RichTextField(blank=True)
    body = StreamField(STANDARD_BLOCKS, use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("header_bg_color"),
                FieldPanel("subheader_bg_color"),
                FieldPanel("subheader_image"),
            ],
            heading="Header & subheader strip",
            classname="collapsible",
        ),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    template = 'home/standard_page.html'


@register_setting
class SiteSettings(BaseSiteSetting):
    # ── Typography ───────────────────────────────────────────
    # Three independent font choices, all from FONT_STACKS (local/system fonts only).
    # Leaving a field blank keeps the CSS file default.

    font_header = models.CharField(
        max_length=64,
        blank=True,
        default="",
        choices=FONT_STACK_CHOICES,
        verbose_name="Site header font",
        help_text="Font for the navigation bar and logo. Leave blank for the CSS default.",
    )
    font_heading = models.CharField(
        max_length=64,
        blank=True,
        default="",
        choices=FONT_STACK_CHOICES,
        verbose_name="Heading font (h1–h6 + page titles)",
        help_text="Applied universally to all headings and page titles across the site. Leave blank for the CSS default.",
    )
    font_body = models.CharField(
        max_length=64,
        blank=True,
        default="",
        choices=FONT_STACK_CHOICES,
        verbose_name="Body text font",
        help_text="Font for all paragraph and general page text. Leave blank for the CSS default.",
    )

    @property
    def font_header_stack(self):
        """CSS font-family value for --font-header, or None if unset."""
        return FONT_STACKS[self.font_header]["stack"] if self.font_header else None

    @property
    def font_heading_stack(self):
        """CSS font-family value for --font-heading, or None if unset."""
        return FONT_STACKS[self.font_heading]["stack"] if self.font_heading else None

    @property
    def font_body_stack(self):
        """CSS font-family value for --font-body, or None if unset."""
        return FONT_STACKS[self.font_body]["stack"] if self.font_body else None

    @property
    def font_css(self):
        """Ready-to-inject CSS :root block overriding the three font variables.
        Returns a mark_safe string so the template can output it directly.
        Returns empty string if no font choices have been saved."""
        from django.utils.safestring import mark_safe
        parts = []
        for field, var in [
            ("font_header",  "--font-header"),
            ("font_heading", "--font-heading"),
            ("font_body",    "--font-body"),
        ]:
            key = getattr(self, field)
            if key and key in FONT_STACKS:
                parts.append(f"{var}: {FONT_STACKS[key]['stack']};")
        if not parts:
            return ""
        return mark_safe(":root { " + " ".join(parts) + " }")

    # ── Header ───────────────────────────────────────────────
    site_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Site name",
        help_text="Overrides the Wagtail site name shown in the header. Leave blank to use the default.",
    )
    site_name_css_classes = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Site name CSS classes",
        help_text="Space-separated CSS classes on the site name text, e.g. 'text-xl font-bold u-color-accent'",
    )
    header_icon = models.ForeignKey(
        get_image_model_string(), null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
        verbose_name="Header icon",
    )
    header_icon_css_classes = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Header icon CSS classes",
        help_text="Space-separated CSS classes on the header icon image, e.g. 'rounded-full'",
    )

    # ── Footer ───────────────────────────────────────────────
    footer_text = RichTextField(
        blank=True,
        default="Neil Whittaker. Built with Wagtail.",
        verbose_name="Footer text",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("font_header"),
                FieldPanel("font_heading"),
                FieldPanel("font_body"),
            ],
            heading="Typography",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("site_name"),
                FieldPanel("site_name_css_classes"),
                FieldPanel("header_icon"),
                FieldPanel("header_icon_css_classes"),
            ],
            heading="Header",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("footer_text"),
            ],
            heading="Footer",
            classname="collapsible",
        ),
    ]

    class Meta:
        verbose_name = "Site Settings"
