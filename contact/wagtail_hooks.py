from django.urls import path
from wagtail import hooks
from . import views


@hooks.register("register_admin_urls")
def register_contact_submission_detail_url():
    return [
        path(
            "contact-submissions/<int:page_pk>/<int:submission_pk>/",
            views.submission_detail,
            name="contact_submission_detail",
        ),
    ]
