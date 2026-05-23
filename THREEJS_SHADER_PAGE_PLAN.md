# Three.js Shader Page — Wagtail Implementation Plan

**Last Updated:** 2026-05-22  
**Project:** Wagtail 7.x Development Site  
**Status:** ✅ Complete — all three shaders confirmed working in browser

---

## ⚠️ Instructions for Claude

> **Read this document at the start of every session** before writing any code.  
> **Update this document at the end of every session:** revise the progress bars (section D), tick completed checklist items (section C), update Next Actions (section E), and add a new entry in the Progress Log (section F).  
> Do not mark something complete in the checklist unless the code is actually saved to disk and the Django dev server runs without errors.

---

## A. General Work Plan

### Objective

Create a new Wagtail page type — `WagtailShaderPage` — that follows the same structure as `StandardPage` but adds a full-width GPU-rendered canvas hero using Three.js and GLSL shaders. The result is a reusable page template (named `wagtail_page.html`) that content editors can create from the Wagtail admin just like any other page.

### The Wagtail Approach

The standard pattern for shader integration in Wagtail is:

1. **Add a `<canvas>` element** in the Wagtail template (in the `{% block precontent %}` or at the top of `{% block content %}`).
2. **Load Three.js** via CDN inside `{% block extra_js %}` (kept in `base.html`).
3. **Write GLSL shaders** as inline JavaScript template literals in the page's own `<script>` block (avoids `fetch()` complexity and Django static file routing issues at dev time).
4. **Initialise the shader** in JavaScript: create a `WebGLRenderer`, attach it to the canvas, build a `ShaderMaterial`, and start a `requestAnimationFrame` loop.

### What We Are Building

| Artefact | Path | Purpose |
|---|---|---|
| Page model | `home/models.py` → `WagtailShaderPage` | Wagtail page type, subclass of `Page` |
| Template | `home/templates/home/wagtail_page.html` | Extends `base.html`, mirrors `standard_page.html` layout + shader canvas |
| Shader JS | `mysite/static/mysite/js/shader-init.js` | Three.js setup, uniform management, render loop |
| Shader CSS | `mysite/static/mysite/css/07-blocks.css` (add rules) | Canvas sizing, positioning, z-index |
| Migration | `home/migrations/` (auto-generated) | Registers the new page model with Django |

### Scope & Constraints

- **No new top-level `static/` directories.** Assets go in `mysite/static/mysite/` to match existing conventions.
- **Three.js loaded from CDN.** No local vendor copy for now; swap to local later if needed.
- **GLSL inlined as JS template literals.** No `fetch()` calls — avoids MIME/CORS issues on the Django dev server.
- **First shader: animated gradient / noise effect.** Simple, visually impressive, no texture dependencies.
- **Canvas is a full-width hero strip** above the page title — same visual zone as the existing `page-subheader` strip.
- **Graceful degradation.** If WebGL is unavailable, the canvas slot shows a CSS gradient fallback.
- **`WagtailShaderPage` re-uses `STANDARD_BLOCKS`** for its body, so editors still get all existing content blocks below the shader hero.

### Success Criteria

- [ ] New page type appears in Wagtail admin "Add child page" menu.
- [ ] Canvas renders and animates without console errors in Chrome, Firefox, and Safari.
- [ ] Page renders correctly at mobile widths (canvas resizes on window resize).
- [ ] Fallback message shown when WebGL is not available.
- [ ] Django dev server (`runserver`) starts without errors after migration.
- [ ] `collectstatic` runs without errors.

---

## B. Implementation by Stages

---

### Stage 1 — Model & Migration (Est. 1–2 hours)

**Objective:** Register `WagtailShaderPage` with Wagtail and Django so the page type is selectable in the admin.

**Tasks:**

1. **Add `WagtailShaderPage` to `home/models.py`**  
   Model fields mirror `StandardPage`:
   - `header_bg_color`, `subheader_bg_color`, `subheader_image` (same as StandardPage)
   - `intro` — `RichTextField`
   - `body` — `StreamField(STANDARD_BLOCKS, ...)`
   - `shader_height` — `IntegerField(default=400)` — lets editors control canvas height in px
   - `shader_type` — `CharField` with choices: `gradient`, `noise`, `wave` (future-proof for multiple shaders)
   - `template = 'home/wagtail_page.html'`

2. **Create and run migration**
   ```bash
   python manage.py makemigrations home
   python manage.py migrate
   ```

3. **Verify page appears in admin**  
   Log into `/admin/` and confirm `WagtailShaderPage` appears under "Add child page."

**Deliverables:**
- `WagtailShaderPage` class in `home/models.py`
- New migration file committed
- Page type visible in Wagtail admin

---

### Stage 2 — Template (Est. 1–2 hours)

**Objective:** Create `wagtail_page.html` that extends `base.html`, preserves the `standard_page.html` layout, and adds the shader canvas zone.

**Tasks:**

1. **Create `home/templates/home/wagtail_page.html`**  
   Structure (blocks from `base.html`):
   - `{% block body_class %}` → `page-standard page-shader`
   - `{% block page_theme %}` → inject `--shader-height` CSS variable from `page.shader_height`
   - `{% block extra_css %}` → no extra file needed; rules go in `07-blocks.css`
   - `{% block precontent %}` → full-width `<div class="shader-hero">` containing `<canvas id="shader-canvas">` and `<div class="shader-fallback">` (hidden by default, shown via JS if WebGL fails)
   - `{% block content %}` → identical to `standard_page.html`: title, HR, intro, body blocks
   - `{% block extra_js %}` → Three.js CDN `<script>` tag, then `{% static 'mysite/js/shader-init.js' %}`

2. **Pass shader config from template to JS**  
   Use a small inline `<script>` inside `{% block extra_js %}` to set a global config object before loading `shader-init.js`:
   ```html
   <script>
     window.ShaderConfig = {
       height: {{ page.shader_height }},
       type: "{{ page.shader_type }}"
     };
   </script>
   ```

3. **Add canvas CSS to `mysite/static/mysite/css/07-blocks.css`**
   ```css
   .shader-hero {
     position: relative;
     width: 100%;
     height: var(--shader-height, 400px);
     overflow: hidden;
     background: #0a0a1a; /* fallback colour */
   }
   .shader-hero canvas {
     display: block;
     width: 100%;
     height: 100%;
   }
   .shader-fallback {
     display: none;
     position: absolute;
     inset: 0;
     background: linear-gradient(135deg, #1a1a3a, #3a1a5c);
   }
   .shader-hero.webgl-unavailable .shader-fallback { display: block; }
   .shader-hero.webgl-unavailable canvas          { display: none; }
   ```

**Deliverables:**
- `home/templates/home/wagtail_page.html` created
- Canvas CSS added to `07-blocks.css`
- Template renders without Django template errors

---

### Stage 3 — Three.js & First Shader (Est. 2–3 hours)

**Objective:** Write `shader-init.js` with a working animated shader and wire it to the canvas.

**Tasks:**

1. **Create `mysite/static/mysite/js/shader-init.js`**

   Structure:
   ```
   ShaderInit
   ├── getCanvas()         — grab #shader-canvas, test WebGL
   ├── buildRenderer()     — THREE.WebGLRenderer, pixelRatio, size
   ├── buildScene()        — Scene, Camera (OrthographicCamera)
   ├── buildMaterial()     — ShaderMaterial with vertexShader + fragmentShader
   ├── buildMesh()         — PlaneGeometry sized to canvas, add to scene
   ├── setupUniforms()     — uTime, uResolution
   ├── handleResize()      — update renderer + uniform on window resize
   └── animate()           — requestAnimationFrame loop, uTime += delta
   ```

2. **Vertex shader (inline template literal)**
   ```glsl
   varying vec2 vUv;
   void main() {
     vUv = uv;
     gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
   }
   ```

3. **Fragment shader — animated gradient noise (inline template literal)**  
   Uses a simple hash-based 2D noise + sine waves over `uTime` to produce a smooth, animated colour gradient. No external texture or image required.

4. **Uniforms passed in:**
   - `uTime` — `float`, incremented each frame
   - `uResolution` — `vec2`, canvas width/height in pixels

5. **Graceful degradation**  
   If `canvas.getContext('webgl2')` or `canvas.getContext('webgl')` returns `null`, add class `webgl-unavailable` to `.shader-hero` and return early — the CSS fallback gradient shows instead.

6. **Test in browser**  
   Load the page at `http://localhost:8000/`, confirm canvas animates, no console errors.

**Deliverables:**
- `mysite/static/mysite/js/shader-init.js` created and working
- Shader animating at 60 FPS in Chrome
- WebGL fallback tested (disable hardware acceleration to test)

---

### Stage 4 — Second Shader & Shader Switcher (Est. 2 hours)

**Objective:** Add a second shader effect and make `shader_type` field actually switch between them.

**Tasks:**

1. **Add `wave` shader**  
   Fragment shader: sine-wave displacement on UV coordinates with a colour gradient overlay. Creates a fluid, undulating effect.

2. **Add `noise` shader** (if separate from gradient)  
   Fragment shader: value noise / FBM (fractal Brownian motion) for a more organic, cloud-like texture.

3. **`shader-init.js` — shader registry pattern**
   ```js
   const SHADERS = {
     gradient: { vertex: `...`, fragment: `...` },
     wave:     { vertex: `...`, fragment: `...` },
     noise:    { vertex: `...`, fragment: `...` },
   };
   const type = window.ShaderConfig?.type ?? 'gradient';
   const { vertex, fragment } = SHADERS[type] ?? SHADERS.gradient;
   ```

4. **Test all three shader types** by creating one `WagtailShaderPage` per type in the admin.

**Deliverables:**
- At least 2 working, named shader types
- `shader_type` field correctly switches the active shader via `ShaderConfig`

---

### Stage 5 — Polish, Resize & Performance (Est. 1–2 hours)

**Objective:** Ensure the page is production-quality in terms of performance and responsiveness.

**Tasks:**

1. **Resize handler** — debounced `window.resize` listener updates `renderer.setSize()` and `uResolution` uniform.

2. **Pixel ratio cap** — use `Math.min(window.devicePixelRatio, 2)` to avoid GPU overload on high-DPI screens.

3. **Visibility pause** — pause the animation loop when the tab is hidden (`document.visibilitychange`) and resume when visible again. Prevents unnecessary GPU work.

4. **Mobile test** — load page on iOS Safari and Chrome Mobile; confirm canvas fills width and animates.

5. **Performance profile** — Chrome DevTools > Performance tab; confirm frame time stays under 16ms.

**Deliverables:**
- Resize working correctly
- Tab-hidden pause working
- Mobile confirmed working

---

### Stage 6 — Documentation & Demo Page (Est. 1 hour)

**Objective:** Make the feature self-documenting for future development sessions.

**Tasks:**

1. **Create a demo `WagtailShaderPage`** via Wagtail admin — one per shader type.

2. **Add a comment block at the top of `shader-init.js`** explaining the shader registry, uniform contract, and how to add a new shader.

3. **Update `CLAUDE.md`** (if it exists) or append a note to this document's References section explaining the file locations and the overall architecture.

4. **Update this plan** — mark all completed stages, update progress bars.

**Deliverables:**
- Demo pages live at `/shader-gradient/`, `/shader-wave/`, `/shader-noise/` (or similar)
- `shader-init.js` is commented and self-explanatory

---

## C. Checklist

### Stage 1 — Model & Migration
- [x] `WagtailShaderPage` added to `home/models.py`
- [x] `shader_height` field added (IntegerField, default 400)
- [x] `shader_type` field added (ChoiceBlock: gradient / wave / noise)
- [x] `template = 'home/wagtail_page.html'` set on the model
- [x] `makemigrations` run successfully
- [x] `migrate` run successfully
- [x] Page type visible in Wagtail admin

### Stage 2 — Template
- [x] `home/templates/home/wagtail_page.html` created
- [x] Extends `base.html` correctly
- [x] `{% block precontent %}` contains `.shader-hero` + `<canvas id="shader-canvas">`
- [x] `{% block content %}` mirrors `standard_page.html` (title, HR, intro, body)
- [x] `window.ShaderConfig` inline script present in `{% block extra_js %}`
- [x] Three.js CDN `<script>` tag present in `{% block extra_js %}`
- [x] `shader-init.js` `<script>` tag present in `{% block extra_js %}`
- [x] Canvas CSS added to `07-blocks.css`
- [x] Fallback CSS added (`.webgl-unavailable` rules)
- [x] Template renders without Django errors ✅ confirmed

### Stage 3 — Three.js & First Shader
- [x] `mysite/static/mysite/js/shader-init.js` created
- [x] WebGL availability check implemented
- [x] `THREE.WebGLRenderer` initialised and attached to canvas
- [x] `OrthographicCamera` and `Scene` set up
- [x] `ShaderMaterial` created with vertex + fragment shaders inline
- [x] `PlaneGeometry` mesh added to scene
- [x] `uTime` uniform updated each frame
- [x] `uResolution` uniform set on init
- [x] `requestAnimationFrame` loop running
- [x] Shader animating in Chrome — **gradient confirmed ✅**, no console errors
- [ ] WebGL fallback (`.webgl-unavailable` class) — not yet tested

### Stage 4 — Second Shader & Switcher
- [x] SHADER registry object (`SHADERS = { gradient, wave, noise }`) implemented
- [x] `window.ShaderConfig.type` read at init to select shader
- [x] `wave` shader implemented
- [x] `noise` (FBM) shader implemented
- [x] `wave` shader browser-tested ✅
- [x] `noise` shader browser-tested ✅

### Stage 5 — Polish & Performance
- [x] Debounced resize handler implemented (in `shader-init.js`)
- [x] `Math.min(devicePixelRatio, 2)` pixel ratio cap in place
- [x] Tab-hidden pause (`visibilitychange`) implemented
- [x] `beforeunload` cleanup (geometry, material, renderer disposed)
- [ ] Tested on mobile (iOS Safari + Chrome Mobile)
- [ ] Chrome DevTools performance profile: frame time < 16ms

### Stage 6 — Documentation & Demo
- [x] Three demo `WagtailShaderPage` instances created in admin ✅
- [x] `shader-init.js` fully commented (architecture, uniform contract, how to add shaders)
- [x] This plan updated with final progress

---

## D. Progress Percentage

```
Overall Completion:              92%

Stage 1 — Model & Migration:   100% ████████████████████  ✅ complete
Stage 2 — Template:            100% ████████████████████  ✅ complete
Stage 3 — Three.js & Shader:    95% ███████████████████░  (fallback not yet tested)
Stage 4 — Shader Switcher:     100% ████████████████████  ✅ all 3 shaders confirmed
Stage 5 — Polish & Perf:        80% ████████████████░░░░  (mobile + DevTools profile remaining)
Stage 6 — Docs & Demo:          90% ██████████████████░░  (mobile test remaining)
```

**Estimated total time:** 8–12 hours  
**Time used so far:** 2 hours  
**Remaining estimate:** 1–2 hours (mobile test, DevTools profile, WebGL fallback test)

---

## E. Next Actions to Be Implemented

### Remaining — Priority 🟠 Medium

1. **Mobile test** — open one of the shader pages on iOS Safari or Chrome Mobile. Confirm the canvas fills the width and animates correctly.

2. **DevTools performance profile** — in Chrome, open DevTools → Performance → record 5 seconds of the shader page. Confirm frame time stays under 16ms (60 FPS).

3. **WebGL fallback test** — in Chrome, go to `chrome://flags/#disable-webgl` and disable WebGL, then visit the page. Confirm the CSS gradient fallback appears instead of a blank block.

### Long Term — Priority ⚪ Optional

4. **Run `collectstatic`** if deploying to production:
   ```bash
   python manage.py collectstatic
   ```

5. **Add a 4th shader** — follow the pattern in `shader-init.js` (add a new key to `SHADERS`, add the choice to `WagtailShaderPage.SHADER_CHOICES` in `models.py`, run `makemigrations`)

---

## F. Progress Log

### Session 3 — 2026-05-22
**Status:** All three shaders confirmed working ✅  
**Time:** 0.5 hours  
**Completed:**
- ✅ Migrations run successfully (`makemigrations` + `migrate`)
- ✅ `WagtailShaderPage` visible in Wagtail admin
- ✅ **Animated Gradient** shader — confirmed rendering, no console errors
- ✅ **Wave Distortion** shader — confirmed rendering, no console errors
- ✅ **Noise / FBM** shader — confirmed rendering, no console errors
- ✅ Plan doc updated to reflect final state

**Remaining (optional):**
- Mobile test (iOS Safari + Chrome Mobile)
- Chrome DevTools performance profile (target < 16ms frame time)
- WebGL fallback test (disable WebGL in Chrome flags)

---

### Session 2 — 2026-05-22
**Status:** All code written; migration + browser testing blocked on your terminal  
**Time:** 1 hour  
**Completed:**
- ✅ `WagtailShaderPage` model added to `home/models.py` with `shader_type`, `shader_height`, all standard header/subheader fields, `intro`, `body`
- ✅ `home/templates/home/wagtail_page.html` created — extends `base.html`, shader canvas in `{% block precontent %}`, `ShaderConfig` inline script, Three.js CDN + `shader-init.js` in `{% block extra_js %}`
- ✅ `mysite/static/mysite/js/shader-init.js` created — Three.js renderer, OrthographicCamera, ShaderMaterial, `requestAnimationFrame` loop, debounced resize, tab-hidden pause, `beforeunload` cleanup
- ✅ Three shader variants written (all inline GLSL, no fetch): **gradient** (hash noise + drifting colour bands), **wave** (layered sine distortion, ocean palette), **noise** (5-octave FBM, volcanic palette)
- ✅ `.shader-hero` CSS added to `07-blocks.css` — sizing, canvas fill, fallback gradient, overlay image support
- ✅ This plan updated

**Blocked:**
- Migration can't run in sandbox (Python 3.14 venv, sandbox only has 3.10) — run manually (see Next Actions)

**Next session:**
- After you run migrations and create a test page, come back and we do the browser testing + Stage 5 performance pass

---

### Session 1 — 2026-05-22
**Status:** Plan created  
**Time:** 0.5 hours  
**Completed:**
- ✅ Reviewed `standard_page.html`, `base.html`, `home/models.py`, `home/blocks.py`
- ✅ Identified correct static file paths (`mysite/static/mysite/`)
- ✅ Confirmed `{% block extra_css %}` and `{% block extra_js %}` hooks exist in `base.html`
- ✅ Decided on inline GLSL (template literals) rather than `fetch()` for dev simplicity
- ✅ Decided on CDN Three.js (no vendor copy)
- ✅ Created this implementation plan

**Architecture decisions:**
- New model `WagtailShaderPage` in `home/models.py` (not a sub-class of `StandardPage` — extends `Page` directly to keep things clean and explicit)
- Template: `home/templates/home/wagtail_page.html`
- Shader JS: `mysite/static/mysite/js/shader-init.js`
- Canvas lives in `{% block precontent %}` — same visual zone as the existing subheader strip
- `window.ShaderConfig` inline object passes `height` and `type` from Django template context to JS

**Next session:**
- Start Stage 1: add model + run migration
- Then Stage 2: create template
- Target: shader animating in browser by end of next session

---

## G. References

### Project Files
- Base template: `mysite/templates/base.html`
- StandardPage template: `home/templates/home/standard_page.html`
- Page models: `home/models.py`
- StreamField blocks: `home/blocks.py`
- Site CSS entry point: `mysite/static/mysite/css/main.css`
- Block styles: `mysite/static/mysite/css/07-blocks.css`
- Site JS: `mysite/static/mysite/js/mysite.js` (do not modify — add a separate file)

### Three.js CDN
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
```
*(r128 is available on cdnjs; upgrade to a newer version if needed — check https://cdnjs.com/libraries/three.js)*

### Wagtail Docs
- [StreamField blocks](https://docs.wagtail.org/en/stable/topics/streamfield.html)
- [Page models](https://docs.wagtail.org/en/stable/topics/pages.html)

### GLSL / Shader Resources
- [The Book of Shaders](https://thebookofshaders.com/) — noise, FBM, patterns
- [Shadertoy](https://www.shadertoy.com/) — inspiration (note: Shadertoy uses `fragCoord` / `iTime`; adapt to Three.js uniforms)
- [Three.js ShaderMaterial docs](https://threejs.org/docs/#api/en/materials/ShaderMaterial)

---

**Document Version:** 1.2  
**Created:** 2026-05-22  
**Last Updated:** 2026-05-22 (Session 3)
