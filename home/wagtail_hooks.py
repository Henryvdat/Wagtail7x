from django.urls import path
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.utils.safestring import mark_safe
from home import views


# ── Homepage link at top of admin sidebar ─────────────────────────────────

@hooks.register("insert_global_admin_css")
def admin_sidebar_home_link_css():
    return mark_safe("""
<style>
/* ── View Site link — sits above the Wagtail bird icon ─────────────────── */
#wt-home-link {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.6rem 1.1rem;
    color: #8fa3c4;
    text-decoration: none;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    transition: background 0.15s, color 0.15s;
    white-space: nowrap;
    overflow: hidden;
}
#wt-home-link:hover {
    background: rgba(255, 255, 255, 0.07);
    color: #cdd6f4;
}
#wt-home-link .wt-home-icon {
    font-size: 1rem;
    flex-shrink: 0;
    line-height: 1;
}
#wt-home-link .wt-home-label {
    opacity: 1;
    transition: opacity 0.15s;
    white-space: nowrap;
}
/* Hide label when sidebar is collapsed */
.sidebar--collapsed #wt-home-link .wt-home-label {
    opacity: 0;
    width: 0;
    overflow: hidden;
}
</style>
""")


@hooks.register("insert_global_admin_js")
def admin_sidebar_home_link_js():
    return mark_safe("""
<script>
(function () {
    'use strict';

    function injectHomeLink() {
        if (document.getElementById('wt-home-link')) return;
        var brand = document.querySelector('a.sidebar-wagtail-branding');
        if (!brand) return;

        var link = document.createElement('a');
        link.id = 'wt-home-link';
        link.href = '/';
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.title = 'View homepage';
        link.innerHTML =
            '<span class="wt-home-icon">&#127968;</span>' +
            '<span class="wt-home-label">View site</span>';

        brand.parentElement.insertBefore(link, brand);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectHomeLink);
    } else {
        injectHomeLink();
    }
})();
</script>
""")


# ── Stylesheet editor — URL + sidebar entry ───────────────────────────────

@hooks.register("register_admin_urls")
def register_stylesheet_urls():
    return [
        path("stylesheets/", views.stylesheet_editor, name="stylesheet_editor"),
    ]


@hooks.register("register_admin_menu_item")
def register_stylesheet_menu_item():
    return MenuItem(
        "Stylesheets",
        "/admin/stylesheets/",
        icon_name="code",
        order=9500,
    )


@hooks.register("insert_global_admin_css")
def block_styles_admin_css():
    return mark_safe("""
<style>
/* ── Block Styles accordion panel ───────────────────────────────────────── */

/* Hide Wagtail's default h3 label — our JS toggle button replaces it */
.block-styles-struct > h3,
.block-styles-struct > [data-streamfield-block-toggle] {
    display: none !important;
}

/* Accordion toggle button */
.block-styles-toggle {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    width: 100%;
    background: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 0.35rem 0.6rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: #555;
    cursor: pointer;
    text-align: left;
    transition: background 0.15s, border-color 0.15s;
    margin-top: 0.5rem;
}
.block-styles-toggle:hover {
    background: #e5e5e5;
    border-color: #c5c5c5;
    color: #333;
}
.block-styles-toggle[aria-expanded="true"] {
    border-radius: 4px 4px 0 0;
    background: #e8e8e8;
    border-color: #ccc;
    border-bottom-color: transparent;
}
.block-styles-toggle .bs-arrow {
    font-size: 0.7rem;
    transition: transform 0.15s;
    display: inline-block;
    width: 0.8rem;
    flex-shrink: 0;
}
.block-styles-toggle[aria-expanded="true"] .bs-arrow {
    transform: rotate(90deg);
}
.block-styles-toggle .bs-label {
    flex: 1;
}
/* Small "cog" icon before label (uses Wagtail's icon font if available, else ⚙) */
.block-styles-toggle::before {
    content: "⚙";
    font-size: 0.75rem;
    opacity: 0.5;
}

/* Fields panel — shown/hidden by JS */
.block-styles-struct > .fields {
    border: 1px solid #ccc;
    border-top: none;
    border-radius: 0 0 4px 4px;
    background: #fafafa;
    overflow: hidden;
}

/* Tighter vertical rhythm inside the open panel */
.block-styles-struct > .fields > li {
    padding-block: 0.3rem;
    padding-inline: 0.5rem;
}
.block-styles-struct > .fields > li + li {
    margin-top: 0;
    border-top: 1px solid #ebebeb;
}

/* Inline label + input on one row */
.block-styles-struct .field-content,
.block-styles-struct .field {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.4rem;
}
.block-styles-struct .field-content label,
.block-styles-struct .field > label {
    min-width: 9rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: #666;
    margin-bottom: 0;
    flex-shrink: 0;
}
.block-styles-struct input[type="text"] {
    flex: 1;
    min-width: 8rem;
    padding: 0.25rem 0.5rem;
    font-size: 0.85rem;
    height: 2rem;
}

/* Checkboxes inline */
.block-styles-struct input[type="checkbox"] {
    width: 1.1rem;
    height: 1.1rem;
    margin: 0;
}

/* Suppress verbose help text */
.block-styles-struct .field-content .help {
    display: none;
}
</style>
""")


@hooks.register("insert_global_admin_js")
def block_styles_admin_js():
    return mark_safe("""
<script>
(function () {
    'use strict';

    function initAccordions() {
        document.querySelectorAll('.block-styles-struct:not([data-bs-init])').forEach(function (block) {
            block.dataset.bsInit = '1';

            var fields = block.querySelector(':scope > .fields');
            if (!fields) return;

            // Start collapsed
            fields.style.display = 'none';

            // Build toggle button
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'block-styles-toggle';
            btn.setAttribute('aria-expanded', 'false');
            btn.innerHTML = '<span class="bs-arrow">&#9658;</span><span class="bs-label">Block styles</span>';

            btn.addEventListener('click', function () {
                var open = fields.style.display !== 'none';
                fields.style.display = open ? 'none' : '';
                btn.setAttribute('aria-expanded', String(!open));
            });

            // Insert the button just before the fields list
            block.insertBefore(btn, fields);
        });
    }

    // Run on initial load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAccordions);
    } else {
        initAccordions();
    }

    // Re-run whenever new blocks are added dynamically (StreamField "Add block" button)
    var observer = new MutationObserver(function (mutations) {
        var needsInit = false;
        mutations.forEach(function (m) {
            m.addedNodes.forEach(function (node) {
                if (node.nodeType === 1) {
                    if (node.classList.contains('block-styles-struct') ||
                        (node.querySelector && node.querySelector('.block-styles-struct'))) {
                        needsInit = true;
                    }
                }
            });
        });
        if (needsInit) initAccordions();
    });

    document.addEventListener('DOMContentLoaded', function () {
        observer.observe(document.body, { childList: true, subtree: true });
    });
})();
</script>
""")


# ── Sitemap / page tree ───────────────────────────────────────────────────

@hooks.register("register_admin_urls")
def register_sitemap_urls():
    return [
        path("sitemap/", views.sitemap_view, name="sitemap_view"),
    ]


@hooks.register("register_admin_menu_item")
def register_sitemap_menu_item():
    return MenuItem(
        "Sitemap",
        "/admin/sitemap/",
        icon_name="site",
        order=9400,
    )
