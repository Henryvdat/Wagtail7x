from django.db import models

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey


class ContactFormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class ContactPage(AbstractEmailForm):
    """
    A contact form page.  Submissions are stored automatically by Wagtail
    under Snippets → Forms in the admin.  The page editor can add / remove
    fields without any code changes.
    """

    intro = RichTextField(
        blank=True,
        help_text="Optional introductory text shown above the form.",
    )
    thank_you_text = RichTextField(
        blank=True,
        help_text="Text shown after a successful submission.",
    )

    # AbstractEmailForm fields (to / from address, subject) are already
    # included in the panel list by default; we append our custom ones.
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldPanel("from_address"),
                FieldPanel("to_address"),
                FieldPanel("subject"),
            ],
            heading="Email notification (optional)",
        ),
    ]

    class Meta:
        verbose_name = "Contact page"
