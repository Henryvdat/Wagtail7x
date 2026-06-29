import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from wagtail.contrib.forms.views import SubmissionsListView


class ContactSubmissionsListView(SubmissionsListView):
    """Submissions list where the first column is a clickable link to the detail view."""

    results_template_name = "contact/admin/list_submissions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Attach a detail URL to every row so the template can render links.
        for row in context.get("data_rows", []):
            row["detail_url"] = reverse(
                "contact_submission_detail",
                args=(self.form_page.pk, row["model_id"]),
            )
        return context


@login_required
def submission_detail(request, page_pk, submission_pk):
    """Admin view: display all fields of a single contact form submission."""
    from .models import ContactPage

    page = get_object_or_404(ContactPage, pk=page_pk)

    # Only staff / users who can manage forms should see this.
    if not request.user.is_staff:
        raise PermissionDenied

    submission = get_object_or_404(
        page.get_submission_class(), pk=submission_pk, page=page
    )

    form_data = submission.get_data()
    data_fields = dict(page.get_data_fields())

    fields = [
        {"label": data_fields.get(key, key.replace("_", " ").title()), "value": value}
        for key, value in form_data.items()
    ]

    return render(
        request,
        "contact/admin/submission_detail.html",
        {
            "form_page": page,
            "submission": submission,
            "fields": fields,
            "list_url": reverse("wagtailforms:list_submissions", args=(page_pk,)),
        },
    )
