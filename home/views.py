import json
import sys
from pathlib import Path

from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Root of the editable CSS files (source, not collected)
CSS_ROOT = Path(settings.BASE_DIR) / "mysite" / "static" / "mysite" / "css"


def _require_superuser(view_fn):
    """Decorator: 403 unless the user is authenticated AND a superuser."""
    from functools import wraps

    @wraps(view_fn)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseForbidden("Superuser access required.")
        return view_fn(request, *args, **kwargs)

    return wrapper


def _build_tree(root: Path):
    """
    Return a list representing the file tree under *root*.
    Each entry is either:
      {"type": "file", "rel": "01-settings.css", "name": "01-settings.css"}
      {"type": "dir",  "name": "pages", "children": [...]}
    Sorted: files before directories at each level, then alphabetically.
    """
    entries = []
    dirs = []
    files = []
    for item in sorted(root.iterdir()):
        if item.suffix == ".css":
            files.append(item)
        elif item.is_dir():
            dirs.append(item)

    # Files first (root level), then directories
    for f in files:
        entries.append({"type": "file", "rel": f.name, "name": f.name})

    for d in dirs:
        children = []
        for f in sorted(d.glob("*.css")):
            rel = f"{d.name}/{f.name}"
            children.append({"type": "file", "rel": rel, "name": f.name})
        if children:
            entries.append({"type": "dir", "name": d.name, "children": children})

    return entries


def _validate_path(rel: str) -> Path | None:
    """
    Resolve *rel* against CSS_ROOT and verify it stays inside CSS_ROOT
    and is a .css file.  Returns the resolved Path or None if invalid.
    """
    try:
        target = (CSS_ROOT / rel).resolve()
    except Exception:
        return None
    if not str(target).startswith(str(CSS_ROOT.resolve())):
        return None
    if target.suffix != ".css":
        return None
    return target


@_require_superuser
def stylesheet_editor(request):
    """
    GET  /admin/stylesheets/                → render editor page
    GET  /admin/stylesheets/?file=<rel>     → return file content as JSON (Ajax)
    POST /admin/stylesheets/                → save file + collectstatic, return JSON
    """
    # ── AJAX file load ──────────────────────────────────────────────────────
    if request.method == "GET" and request.GET.get("file"):
        rel = request.GET["file"]
        path = _validate_path(rel)
        if path is None or not path.exists():
            return JsonResponse({"error": "File not found."}, status=404)
        return JsonResponse({"content": path.read_text(encoding="utf-8"), "file": rel})

    # ── Save ────────────────────────────────────────────────────────────────
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

        rel = data.get("file", "")
        content = data.get("content", "")
        path = _validate_path(rel)
        if path is None:
            return JsonResponse({"error": "Invalid file path."}, status=400)

        path.write_text(content, encoding="utf-8")

        # Run collectstatic so the collected static/ folder stays in sync
        import subprocess

        manage_py = Path(settings.BASE_DIR) / "manage.py"
        try:
            result = subprocess.run(
                [sys.executable, str(manage_py), "collectstatic", "--noinput"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
            msg = lines[-1] if lines else "collectstatic complete."
            if result.returncode != 0:
                msg = f"Saved (collectstatic error: {result.stderr[:120]})"
        except Exception as exc:
            msg = f"Saved (collectstatic skipped: {exc})"

        return JsonResponse({"ok": True, "message": msg})

    # ── Render page ─────────────────────────────────────────────────────────
    tree = _build_tree(CSS_ROOT)
    return render(
        request,
        "home/admin/stylesheet_editor.html",
        {
            "tree_json": json.dumps(tree),
            "css_root_display": str(CSS_ROOT.relative_to(Path(settings.BASE_DIR))),
        },
    )
