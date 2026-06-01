# Read More Button — Implementation Plan

> **Last updated:** 2026-05-22  
> **Overall progress:** 75 % (all code complete; `migrate` + live browser test still pending)  
> **Status:** In Progress

### Bug fixes applied this session
- **Root cause of missing button styles:** All CSS edits were going to `STATIC_ROOT` (`/static/mysite/css/`) instead of the source `STATICFILES_DIRS` (`/mysite/static/mysite/css/`). Django dev server only serves from the latter. All CSS changes have now been applied to the correct source directory.
- **Hover lift removed:** `transform: translateY(-2px)` removed from `.blog-listing__item:hover` in `mysite/static/mysite/css/pages/blog.css` — cards no longer jump upward on hover.
- **Blog index "Read more" button:** Template updated to use `btn-read-more btn-read-more--solid`; conflicting `a:last-child` rule replaced with `.blog-listing__body .btn-read-more` positioning rule.

---

## a) General Work Plan

### What we're building
A reusable `ReadMoreButtonBlock` — a Wagtail `StructBlock` that renders a styled `<a>` (semantically correct for navigation, visually a button) with:

| Feature | Detail |
|---|---|
| **Customisable text** | Free-text `CharBlock`, default "Read more" |
| **Page target** | `PageChooserBlock` — any published page in the site |
| **Style options** | Piggybacks on the existing `BlockStylesBlock` (bg colour, text colour, border, CSS classes) |
| **Alignment** | Reuses `ALIGNMENT_CHOICES` (left / center / right / full) |
| **Button style variant** | `ChoiceBlock`: solid / outline / ghost |
| **Placement** | Added to `STANDARD_BLOCKS` (body of every page type) AND to `ColumnContentBlock` (so it can sit inside 2- and 3-column layouts) |

### Codebase touch-points (from reading the project)
| File | Change | Status |
|---|---|---|
| `home/blocks.py` | New `ReadMoreButtonBlock`; add entry to `STANDARD_BLOCKS` and `ColumnContentBlock` | ✅ Done |
| `home/templates/home/blocks/read_more_button.html` | New template | ✅ Done |
| `static/mysite/css/07-blocks.css` | Button styles (`.btn-read-more`, variants) | ✅ Done |
| `home/migrations/0025_add_read_more_button_block.py` | Migration for HomePage + StandardPage | ✅ Done |
| `blog/migrations/0024_add_read_more_button_block.py` | Migration for BlogIndexPage + BlogPage | ✅ Done |

---

## b) Implementation by Stages

### Stage 1 — Block definition (`home/blocks.py`) ✅
- [x] Add `PageChooserBlock` import from `wagtail.blocks`
- [x] Define `ReadMoreButtonBlock(StructBlock)` with fields:
  - `button_text` — `CharBlock(default='Read more', max_length=100)`
  - `page` — `PageChooserBlock()`
  - `button_style` — `ChoiceBlock([solid, outline, ghost], default='solid')`
  - `alignment` — `ChoiceBlock(ALIGNMENT_CHOICES, default='left')`
  - `styles` — `BlockStylesBlock(required=False)`
- [x] Set `Meta`: `template`, `icon='link'`, `label='Read More Button'`
- [x] Add `('read_more_button', ReadMoreButtonBlock())` to `STANDARD_BLOCKS`
- [x] Add `read_more_button = ReadMoreButtonBlock()` to `ColumnContentBlock`

### Stage 2 — Template ✅
- [x] Create `home/templates/home/blocks/read_more_button.html`
- [x] Use `{% pageurl value.page %}` for the href
- [x] Apply alignment wrapper class `block-align--{{ value.alignment }}`
- [x] Apply `btn-read-more btn-read-more--{{ value.button_style }}` classes
- [x] Merge `BlockStylesBlock` inline styles (background, text colour, border)
- [x] Apply any extra `custom_classes`
- [x] Render `{{ value.button_text }}` as the link text

### Stage 3 — CSS ✅
- [x] Add `.btn-read-more` base styles to `static/mysite/css/07-blocks.css`
- [x] Add `.btn-read-more--solid` variant (filled accent background)
- [x] Add `.btn-read-more--outline` variant (transparent + border)
- [x] Add `.btn-read-more--ghost` variant (text-only, hover underline)
- [x] Styles compose cleanly with `BlockStylesBlock` inline overrides; focus ring for accessibility

### Stage 4 — Migration ✅
- [x] `home/migrations/0025_add_read_more_button_block.py` hand-crafted (Django 6 / Python 3.12 venv not available in sandbox)
- [x] `blog/migrations/0024_add_read_more_button_block.py` hand-crafted (covers BlogIndexPage + BlogPage)
- [x] Both migration files reviewed and syntax-verified
- [ ] `python manage.py migrate` applied on live server ← **run this when server starts**

### Stage 5 — Verification (pending live server)
- [ ] Start dev server (`python manage.py runserver`)
- [ ] Open Wagtail admin → edit a HomePage or StandardPage body
- [ ] Confirm "Read More Button" appears in the block chooser
- [ ] Add a block, choose a page, set text, save/publish
- [ ] View the page on the frontend — button appears, click navigates correctly
- [ ] Test inside a Two Column block (ColumnContentBlock)
- [ ] Test all three button style variants
- [ ] Test BlockStylesBlock overrides (custom bg colour, CSS class)

---

## c) Checklist

### Stage 1 — Block definition
- [x] `PageChooserBlock` imported
- [x] `ReadMoreButtonBlock` class defined with all 5 fields
- [x] Added to `STANDARD_BLOCKS`
- [x] Added to `ColumnContentBlock`

### Stage 2 — Template
- [x] File created at correct path
- [x] `{% load wagtailcore_tags %}` present
- [x] `{% pageurl value.page %}` used for href
- [x] Alignment class applied
- [x] Button style variant class applied
- [x] Inline styles from `BlockStylesBlock` applied
- [x] Custom classes applied
- [x] Button text rendered

### Stage 3 — CSS
- [x] Base `.btn-read-more` rule added
- [x] `--solid` variant added
- [x] `--outline` variant added
- [x] `--ghost` variant added
- [x] No conflicts with existing block classes

### Stage 4 — Migration
- [x] Migration files written (home 0025, blog 0024)
- [x] Migration files syntax-verified
- [ ] `python manage.py migrate` applied on live server

### Stage 5 — Verification
- [ ] Block appears in admin chooser
- [ ] Block saves and publishes without error
- [ ] Frontend renders correctly
- [ ] Page link navigates correctly
- [ ] Works inside column blocks
- [ ] All 3 style variants render correctly
- [ ] BlockStylesBlock overrides work

---

## d) Progress Percentage

| Stage | Tasks | Done | % |
|---|---|---|---|
| Stage 1 — Block definition | 4 | 4 | 100% |
| Stage 2 — Template | 8 | 8 | 100% |
| Stage 3 — CSS | 5 | 5 | 100% |
| Stage 4 — Migration | 3 | 2 | 67% |
| Stage 5 — Verification | 7 | 0 | 0% |
| **TOTAL** | **27** | **19** | **70%** |

---

## e) Next Actions

**All code is written. One manual step remains before verification:**

1. **Run migrations** — in your project terminal (with venv active):
   ```
   python manage.py migrate
   ```
2. **Start the dev server** and open the admin to verify the block appears
3. **Test all three button style variants** — solid, outline, ghost
4. **Test inside a column block** (Two Columns → left or right column)
5. **Tick off Stage 5 checklist items** above and update progress to 100%

---

## f) Claude self-update instruction

> **At the end of every session that touches this feature, Claude must:**
>
> 1. Update the `Last updated` date at the top of this file to today's date
> 2. Tick off completed checklist items (change `- [ ]` → `- [x]`)
> 3. Recalculate the "Done" column and % in the Progress table
> 4. Update the **Overall progress** percentage at the top
> 5. Update **Status** (Planning → In Progress → Complete)
> 6. Replace the **Next Actions** section with what remains undone
>
> This file is the single source of truth for this feature's progress.
