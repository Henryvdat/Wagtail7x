/**
 * shader-init.js
 * ==============
 * Initialises a Three.js WebGL shader hero on WagtailShaderPage.
 *
 * HOW IT WORKS
 * ------------
 * 1. window.ShaderConfig is set inline by wagtail_page.html before this script loads.
 *    It provides { type: "gradient"|"wave"|"noise"|"accretion", height: <number> }.
 * 2. A THREE.WebGLRenderer is attached to #shader-canvas.
 * 3. An OrthographicCamera + PlaneGeometry fills the canvas exactly.
 * 4. A THREE.ShaderMaterial uses one of the SHADERS below.
 * 5. uTime and uResolution uniforms are updated every frame.
 *
 * ADDING A NEW SHADER
 * -------------------
 * Add a new key to the SHADERS object below with { fragment } string.
 * The vertex shader is shared — you only need to write the fragment shader.
 * Then add the key as a choice in WagtailShaderPage.SHADER_CHOICES (home/models.py)
 * and re-run makemigrations.
 *
 * UNIFORM CONTRACT (available in every fragment shader)
 * ----------------
 *   uTime       float   Seconds since page load (increases each frame)
 *   uResolution vec2    Canvas width × height in CSS pixels
 *
 * SHADERTOY ADAPTATION GUIDE
 * --------------------------
 * Rename: iTime → uTime,  iResolution → uResolution
 * Replace mainImage(out vec4 O, vec2 I) signature with:
 *   void main() { vec2 I = vUv * uResolution; vec4 O = vec4(0.0); ... gl_FragColor = O; }
 * Use integer for loops (not float counters) for maximum driver compatibility.
 */

(function () {
  'use strict';

  /* ─────────────────────────────────────────────────────────────────────────
   * SHARED VERTEX SHADER
   * All shaders use this identical passthrough — no need to duplicate it.
   * ───────────────────────────────────────────────────────────────────────── */

  var VERTEX_SHADER = /* glsl */`
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `;


  /* ─────────────────────────────────────────────────────────────────────────
   * SHADER LIBRARY
   * Each entry only needs a { fragment } string — vertex is added automatically.
   * ───────────────────────────────────────────────────────────────────────── */

  var SHADERS = {

    /* ── Animated Gradient ─────────────────────────────────────────────── */
    gradient: {
      fragment: /* glsl */`
        uniform float uTime;
        uniform vec2  uResolution;
        varying vec2  vUv;

        float hash(vec2 p) {
          p = fract(p * vec2(127.1, 311.7));
          p += dot(p, p + 19.19);
          return fract(p.x * p.y);
        }

        float noise(vec2 p) {
          vec2 i = floor(p);
          vec2 f = fract(p);
          vec2 u = f * f * (3.0 - 2.0 * f);
          return mix(
            mix(hash(i + vec2(0.0, 0.0)), hash(i + vec2(1.0, 0.0)), u.x),
            mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x),
            u.y
          );
        }

        void main() {
          vec2  uv = vUv;
          float n  = noise(uv * 2.0 + vec2(uTime * 0.055, uTime * 0.038));
          float t  = uTime * 0.14;

          // Named colours — deep navy through ocean blue to rich teal
          vec3 colDark  = vec3(0.02, 0.06, 0.18);  // near-black navy
          vec3 colOcean = vec3(0.04, 0.20, 0.44);  // deep ocean blue
          vec3 colTeal  = vec3(0.04, 0.38, 0.54);  // rich teal
          vec3 colMid   = vec3(0.07, 0.13, 0.30);  // dark slate blue

          float a = 0.5 + 0.5 * sin(uv.x * 2.6 + t        + n * 1.8);
          float b = 0.5 + 0.5 * sin(uv.y * 2.1 + t * 0.72 + n * 1.4);
          float c = 0.5 + 0.5 * sin((uv.x + uv.y) * 1.7 + t * 1.15 + n * 0.9);

          vec3 col = mix(colDark,  colOcean, a);
               col = mix(col,      colTeal,  b * 0.6);
               col = mix(col,      colMid,   c * 0.45);

          // Vignette — darken edges for cinematic depth
          vec2  ctr  = uv - 0.5;
          float vign = 1.0 - dot(ctr, ctr) * 1.5;
          col *= clamp(vign, 0.45, 1.0);

          gl_FragColor = vec4(col, 1.0);
        }
      `
    },

    /* ── Wave Distortion ───────────────────────────────────────────────── */
    wave: {
      fragment: /* glsl */`
        uniform float uTime;
        uniform vec2  uResolution;
        varying vec2  vUv;

        void main() {
          vec2 uv = vUv;

          float wave1 = sin(uv.x * 10.0 + uTime * 1.2) * 0.04;
          float wave2 = sin(uv.y * 8.0  + uTime * 0.9) * 0.04;
          float wave3 = sin((uv.x + uv.y) * 6.0 + uTime * 0.7) * 0.03;
          vec2 distorted = uv + vec2(wave1 + wave3, wave2 + wave3);

          vec3 colA = vec3(0.05, 0.15, 0.40);
          vec3 colB = vec3(0.10, 0.55, 0.65);
          vec3 colC = vec3(0.85, 0.90, 1.00);

          float t1 = 0.5 + 0.5 * sin(distorted.x * 5.0 + uTime * 0.6);
          float t2 = 0.5 + 0.5 * sin(distorted.y * 4.0 + uTime * 0.4 + 1.0);

          vec3 col = mix(colA, colB, t1);
               col = mix(col,  colC, t2 * 0.35);

          /* Subtle vignette */
          vec2  center = distorted - 0.5;
          float vign   = 1.0 - dot(center, center) * 1.2;
          col *= clamp(vign, 0.0, 1.0);

          gl_FragColor = vec4(col, 1.0);
        }
      `
    },

    /* ── Noise / FBM ───────────────────────────────────────────────────── */
    noise: {
      fragment: /* glsl */`
        uniform float uTime;
        uniform vec2  uResolution;
        varying vec2  vUv;

        vec2 hash2(vec2 p) {
          p = vec2(dot(p, vec2(127.1, 311.7)),
                   dot(p, vec2(269.5, 183.3)));
          return -1.0 + 2.0 * fract(sin(p) * 43758.5453123);
        }

        float valueNoise(vec2 p) {
          vec2 i = floor(p);
          vec2 f = fract(p);
          vec2 u = f * f * (3.0 - 2.0 * f);
          return mix(
            mix(dot(hash2(i + vec2(0.0, 0.0)), f - vec2(0.0, 0.0)),
                dot(hash2(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0)), u.x),
            mix(dot(hash2(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0)),
                dot(hash2(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0)), u.x),
            u.y
          );
        }

        /* 5-octave FBM */
        float fbm(vec2 p) {
          float v   = 0.0;
          float amp = 0.5;
          mat2  rot = mat2(cos(0.5), -sin(0.5), sin(0.5), cos(0.5));
          for (int i = 0; i < 5; i++) {
            v   += amp * valueNoise(p);
            p    = rot * p * 2.1;
            amp *= 0.5;
          }
          return v;
        }

        void main() {
          vec2  uv = vUv * 3.0;
          float t  = uTime * 0.12;
          float f1 = fbm(uv + vec2(t, t * 0.7));
          float f2 = fbm(uv + vec2(f1 * 1.5 + t * 0.4, f1 * 1.2));
          float val = fbm(uv + vec2(f2));

          vec3 colA = vec3(0.05, 0.02, 0.10);
          vec3 colB = vec3(0.55, 0.10, 0.05);
          vec3 colC = vec3(0.95, 0.55, 0.10);
          vec3 colD = vec3(1.00, 0.95, 0.80);

          vec3 col = mix(colA, colB, smoothstep(0.0,  0.35, val));
               col = mix(col,  colC, smoothstep(0.25, 0.65, val));
               col = mix(col,  colD, smoothstep(0.60, 1.00, val));

          gl_FragColor = vec4(col, 1.0);
        }
      `
    },

    /* ── Accretion — shadertoy.com/view/WcKXDV by @XorDev ─────────────────
       Adaptations from original Shadertoy:
         iTime        → uTime
         iResolution  → uResolution
         mainImage()  → main() + gl_FragColor
         float loop counters (i++, d++ in for-condition) → int counters
           — float post-increment in for() is rejected by some WebGL1 drivers
         Chained assignment (z += d = length(...)) → two statements
           — cleaner and avoids ambiguous evaluation order
         tanh() built-in → _tanh() via exp()
           — tanh is GLSL ES 3.0 only; exp() works everywhere
         _tanh input clamped to [-10, 10]
           — prevents exp() overflow on low-end hardware (overflows at ~88)
         Division guarded with max(d, 1e-4)
           — prevents NaN if the raymarch step collapses to zero          */
    accretion: {
      fragment: /* glsl */`
        uniform float uTime;
        uniform vec2  uResolution;
        varying vec2  vUv;

        /* Numerically stable tanh via exp() — works on WebGL1 and WebGL2 */
        vec4 _tanh(vec4 x) {
          x = clamp(x, -10.0, 10.0); /* prevent exp() overflow */
          vec4 e = exp(2.0 * x);
          return (e - 1.0) / (e + 1.0);
        }

        void main() {
          /* Convert normalised UV → pixel coordinates (Shadertoy fragCoord) */
          vec2 I = vUv * uResolution;

          vec4  O = vec4(0.0);
          float z = 0.0;
          float d = 1.0; /* initialise to 1 so first iteration never divides by 0 */

          /* Raymarch — 20 steps using int counter (universally compatible) */
          for (int ii = 0; ii < 20; ii++) {
            float i = float(ii) + 1.0; /* matches original: body sees 1..20 */

            /* Ray sample point */
            vec3 p = z * normalize(vec3(I + I, 0.0) - uResolution.xyx) + 0.1;

            /* Polar coordinates + shape transformations */
            p = vec3(atan(p.y / 0.2, p.x) * 2.0,
                     p.z / 3.0,
                     length(p.xy) - 5.0 - z * 0.2);

            /* Turbulence + refraction (XorDev's key technique) */
            for (int jj = 0; jj < 7; jj++) {
              float dj = float(jj) + 1.0; /* body sees 1..7 */
              p += sin(p.yzx * dj + uTime + 0.3 * i) / dj;
            }

            /* Step distance — guarded against zero */
            d  = max(length(vec4(0.4 * cos(p) - 0.4, p.z)), 1e-4);
            z += d;

            /* Colour accumulation */
            O += (1.0 + cos(p.x + i * 0.4 + z + vec4(6.0, 1.0, 2.0, 0.0))) / d;
          }

          gl_FragColor = _tanh(O * O / 400.0);
        }
      `
    }

  }; /* end SHADERS */


  /* ─────────────────────────────────────────────────────────────────────────
   * WEBGL AVAILABILITY CHECK
   * Use a throwaway canvas — not the shader canvas itself.
   * If we bind a context to the shader canvas here, Three.js gets a second
   * context on the same element which behaves inconsistently across browsers.
   * ───────────────────────────────────────────────────────────────────────── */

  function webglAvailable() {
    try {
      var tmp = document.createElement('canvas');
      return !!(tmp.getContext('webgl2') || tmp.getContext('webgl'));
    } catch (e) {
      return false;
    }
  }


  /* ─────────────────────────────────────────────────────────────────────────
   * INIT
   * ───────────────────────────────────────────────────────────────────────── */

  function init() {
    var config    = window.ShaderConfig || {};
    var type      = config.type || 'gradient';
    var shaderDef = SHADERS[type] || SHADERS.gradient;

    var hero   = document.getElementById('shader-hero');
    var canvas = document.getElementById('shader-canvas');
    if (!hero || !canvas) return;

    if (!webglAvailable()) {
      hero.classList.add('webgl-unavailable');
      return;
    }

    /* ── Dimensions ──
         Use ShaderConfig.height from Django context rather than hero.clientHeight.
         At small heights the CSS variable may not be computed yet when this runs,
         making clientHeight read as 0 and producing a blank canvas. */
    var w = hero.clientWidth || window.innerWidth;
    var h = config.height    || 400;

    /* ── Renderer ── */
    var renderer = new THREE.WebGLRenderer({
      canvas:    canvas,
      antialias: false,
      alpha:     false
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(w, h);

    /* ── Scene & Camera ──
         OrthographicCamera fills the canvas exactly — no perspective distortion. */
    var scene  = new THREE.Scene();
    var camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);

    /* ── Uniforms ── */
    var uniforms = {
      uTime:       { value: 0.0 },
      uResolution: { value: new THREE.Vector2(w, h) }
    };

    /* ── Material & Mesh ── */
    var geometry = new THREE.PlaneGeometry(2, 2);
    var material = new THREE.ShaderMaterial({
      uniforms:       uniforms,
      vertexShader:   VERTEX_SHADER,
      fragmentShader: shaderDef.fragment,
      depthWrite:     false
    });
    scene.add(new THREE.Mesh(geometry, material));

    /* ── Resize handler (debounced 100ms) ──
         Height is fixed by the page model; only width changes on resize. */
    var resizeTimer;
    function onResize() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        var newW = hero.clientWidth || window.innerWidth;
        var newH = config.height    || 400;
        renderer.setSize(newW, newH);
        uniforms.uResolution.value.set(newW, newH);
      }, 100);
    }
    window.addEventListener('resize', onResize);

    /* ── Visibility pause — save GPU when tab is backgrounded ── */
    var paused = false;
    document.addEventListener('visibilitychange', function () {
      paused = document.hidden;
    });

    /* ── Render loop ── */
    var clock     = new THREE.Clock();
    var animFrame = null;

    function animate() {
      animFrame = requestAnimationFrame(animate);
      if (paused) return;
      uniforms.uTime.value = clock.getElapsedTime();
      renderer.render(scene, camera);
    }

    animate();

    /* ── Cleanup on page unload ── */
    window.addEventListener('beforeunload', function () {
      cancelAnimationFrame(animFrame);
      window.removeEventListener('resize', onResize);
      geometry.dispose();
      material.dispose();
      renderer.dispose();
    });
  }

  /* Run after DOM is ready */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

}());
