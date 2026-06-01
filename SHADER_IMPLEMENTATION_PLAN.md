# Shader Implementation Plan for Wagtail Site

**Last Updated:** 2026-05-22  
**Project:** Wagtail 7.x Development Site  
**Status:** 📋 Planning Phase

---

## 📋 Document Instructions

> **⚠️ IMPORTANT:** This plan should be updated at the end of each development session.  
> **For Claude:** Always review this document at the start of each session and update the progress percentage, checklist status, and next actions based on completed work. Update timestamps and add notes in the Progress Log section.

---

## A. General Work Plan

### Overview
Implement WebGL shaders into the Wagtail development site to add dynamic, GPU-accelerated visual effects. The implementation will leverage:

- **Three.js** - WebGL library for 3D rendering
- **GLSL Shaders** - Vertex and fragment shaders for GPU effects
- **Wagtail StreamField** - Custom blocks for shader-based components
- **Static Files** - Django/Wagtail static file management for shader files

### Goals
1. ✅ Establish shader infrastructure in Wagtail project
2. ✅ Create reusable shader components via StreamField blocks
3. ✅ Implement at least 2-3 example shaders
4. ✅ Document shader authoring patterns for future use
5. ✅ Optimize shader loading and rendering performance

### Technology Stack
- **Framework:** Wagtail (Django-based CMS)
- **WebGL Library:** Three.js (latest stable version)
- **Shader Language:** GLSL (evolving toward TSL - Three Shading Language)
- **Asset Management:** Django Static Files (`STATIC_ROOT`, `STATICFILES_DIRS`)
- **Frontend:** Vanilla JavaScript + HTML5 Canvas

### Success Criteria
- [ ] Shaders load without console errors
- [ ] StreamField blocks render canvas elements correctly
- [ ] GPU rendering performs at 60 FPS for demo content
- [ ] Shader code is modular and reusable
- [ ] Documentation is comprehensive for future developers

---

## B. Implementation by Stages

### **Stage 1: Foundation & Setup (Est. 2-3 hours)**

**Objective:** Establish the project structure and dependencies.

**Tasks:**
1. Set up static file directory structure
   - Create `static/js/shaders/` directory
   - Create `static/glsl/` directory for shader files
   - Create `static/js/vendors/` for Three.js

2. Add Three.js to project
   - Option A: Download Three.js library to static files
   - Option B: Use CDN with fallback to local copy
   - Include necessary examples (OrbitControls, etc.)

3. Configure Django static files
   - Verify `STATIC_URL` and `STATIC_ROOT` in settings
   - Update `STATICFILES_DIRS` if needed
   - Ensure collectstatic command works

4. Create base shader infrastructure file
   - `static/js/shader-manager.js` - Central manager for shader compilation and lifecycle

5. Document setup process
   - Write setup guide for future developers

**Deliverables:**
- Project structure ready
- Three.js integrated
- Base shader manager initialized

---

### **Stage 2: Shader Compilation & Loading System (Est. 2-3 hours)**

**Objective:** Build robust shader compilation and asset loading pipeline.

**Tasks:**
1. Create GLSL shader file templates
   - Basic vertex shader template (`static/glsl/vertex.glsl`)
   - Basic fragment shader template (`static/glsl/fragment.glsl`)

2. Develop shader compiler utility
   - `ShaderCompiler` class in `shader-manager.js`
   - Fetch GLSL files at runtime
   - Validate shader compilation
   - Error handling and reporting

3. Implement shader caching strategy
   - Cache compiled shaders to avoid recompilation
   - Version control shader assets

4. Create shader error logger
   - Capture WebGL shader compilation errors
   - Log uniform variable issues
   - Display debugging info (optional console)

5. Build example: Simple color shader
   - Create basic shader that changes canvas color
   - Test compilation and rendering pipeline

**Deliverables:**
- Shader compilation system working
- Error handling in place
- Example shader compiling and rendering

---

### **Stage 3: StreamField Block Integration (Est. 3-4 hours)**

**Objective:** Create Wagtail StreamField blocks for shader content.

**Tasks:**
1. Design custom StreamField block architecture
   - Base abstract block for shaders
   - Configuration options (canvas size, shader type, parameters)

2. Create ShaderBlock StreamField component
   - `blocks/shader_block.py` - Django StreamField block
   - Handles shader selection and configuration
   - Passes data to frontend template

3. Create block template
   - `templates/blocks/shader_block.html`
   - Renders canvas element with unique ID
   - Includes necessary script initialization

4. Implement shader parameter UI
   - Allow non-technical editors to configure shader parameters
   - Support for: float, int, color, vector uniforms
   - Real-time preview in editor (if possible)

5. Register block with pages
   - Add ShaderBlock to page models
   - Test block in Wagtail admin interface

**Deliverables:**
- StreamField block created and functional
- Block appears in Wagtail editor
- Parameters configurable from admin interface
- Block template renders correctly

---

### **Stage 4: Core Shaders Implementation (Est. 4-5 hours)**

**Objective:** Create production-ready shaders.

**Tasks:**
1. **Shader A: Noise/Perlin Effect**
   - Vertex shader: Basic passthrough
   - Fragment shader: 2D noise generation
   - Uniforms: time, scale, color palette
   - Use case: Animated backgrounds, gradients

2. **Shader B: Wave Distortion Effect**
   - Vertex shader: Sine wave displacement
   - Fragment shader: Procedural wave patterns
   - Uniforms: frequency, amplitude, time, color
   - Use case: Water effects, ripples, fluid dynamics

3. **Shader C: Particle System (optional)**
   - Vertex shader: Instanced particle positioning
   - Fragment shader: Particle rendering
   - Uniforms: lifetime, velocity, spawn rate
   - Use case: Fireworks, emitters, dynamic visuals

4. For each shader:
   - Write clean, commented GLSL code
   - Create separate `.glsl` files
   - Test uniform parameter changes
   - Optimize for performance

5. Documentation
   - Parameter guide (what each uniform does)
   - Visual examples
   - Performance notes

**Deliverables:**
- 2-3 production-ready shaders
- Shader files stored in `static/glsl/`
- Shader documentation
- All shaders tested in StreamField blocks

---

### **Stage 5: Performance & Optimization (Est. 2-3 hours)**

**Objective:** Ensure smooth rendering and optimal load times.

**Tasks:**
1. Performance profiling
   - Use Chrome DevTools GPU profiling
   - Measure frame rate, GPU utilization
   - Identify bottlenecks

2. Shader optimization
   - Reduce fragment shader complexity if needed
   - Minimize matrix operations
   - Use efficient texture sampling

3. Memory management
   - Implement proper cleanup (destroy shaders on page exit)
   - Prevent memory leaks in event listeners

4. Responsive canvas sizing
   - Handle window resize events
   - Maintain aspect ratio
   - Mobile/tablet considerations

5. Fallback handling
   - Graceful degradation for non-WebGL browsers
   - Error state display

6. Load time optimization
   - Lazy load shader files
   - Minimize Three.js bundle size
   - Consider using tree-shaking

**Deliverables:**
- Performance benchmarks documented
- Shaders optimized for 60 FPS
- Memory leaks fixed
- Fallback strategies in place

---

### **Stage 6: Documentation & Testing (Est. 2-3 hours)**

**Objective:** Ensure maintainability and ease of future development.

**Tasks:**
1. Code documentation
   - Comment all shader files
   - JSDoc for JavaScript files
   - Document uniform parameters

2. Developer guide
   - How to create new shaders
   - How to add StreamField blocks
   - Troubleshooting guide

3. User guide (for content editors)
   - How to use shader blocks in Wagtail
   - Parameter explanations
   - Best practices for embedding

4. Testing
   - Test all shaders across browsers (Chrome, Firefox, Safari)
   - Test on various devices (desktop, tablet, mobile)
   - Test shader parameter changes

5. Example pages
   - Create demo page with all shaders
   - Show best practices
   - Include variations

6. Update main project documentation
   - Add shader section to main CLAUDE.md

**Deliverables:**
- Complete documentation
- Developer guide published
- All tests passed
- Example pages created

---

## C. Checklist

### Stage 1: Foundation & Setup
- [ ] Static file directory structure created
- [ ] Three.js downloaded/configured
- [ ] Django static files configured
- [ ] Base shader manager file created
- [ ] Setup documentation written

### Stage 2: Shader Compilation & Loading
- [ ] GLSL shader templates created
- [ ] ShaderCompiler class implemented
- [ ] Shader caching system working
- [ ] Error logger functional
- [ ] Example color shader compiling and rendering

### Stage 3: StreamField Integration
- [ ] ShaderBlock component designed
- [ ] ShaderBlock Python class created
- [ ] Block template created and tested
- [ ] Shader parameter UI implemented
- [ ] Block registered and functional in admin

### Stage 4: Core Shaders
- [ ] Noise/Perlin shader complete
- [ ] Wave distortion shader complete
- [ ] Particle system shader (optional) complete
- [ ] All shaders documented
- [ ] All shaders tested in StreamField blocks

### Stage 5: Performance & Optimization
- [ ] Performance profiling completed
- [ ] Shaders optimized for 60 FPS
- [ ] Memory leaks fixed
- [ ] Responsive sizing working
- [ ] Fallback strategies implemented
- [ ] Load times optimized

### Stage 6: Documentation & Testing
- [ ] Code fully documented
- [ ] Developer guide written
- [ ] User guide written
- [ ] Cross-browser testing completed
- [ ] Mobile testing completed
- [ ] Demo pages created
- [ ] Main project documentation updated

---

## D. Progress Percentage

```
Overall Completion: 0%

Foundation & Setup:           0% ░░░░░░░░░░░░░░░░░░░░
Compilation System:           0% ░░░░░░░░░░░░░░░░░░░░
StreamField Integration:      0% ░░░░░░░░░░░░░░░░░░░░
Core Shaders:                 0% ░░░░░░░░░░░░░░░░░░░░
Performance & Optimization:   0% ░░░░░░░░░░░░░░░░░░░░
Documentation & Testing:      0% ░░░░░░░░░░░░░░░░░░░░
```

**Estimated Total Time:** 15-21 hours  
**Current Session Time Used:** 0 hours  
**Remaining Time Estimate:** 15-21 hours

---

## E. Next Actions to be Implemented

### Immediate (Priority: 🔴 High)
1. **Create static file directory structure**
   - Execute bash commands to create directories
   - Verify directory paths and permissions

2. **Set up Three.js integration**
   - Download Three.js library OR configure CDN
   - Test Three.js loads correctly

3. **Initialize base shader manager**
   - Create `static/js/shader-manager.js`
   - Implement basic ShaderCompiler class

### Short Term (Priority: 🟠 Medium)
1. **Build shader loading system**
   - Create GLSL template files
   - Implement fetch + compilation pipeline

2. **Design StreamField blocks**
   - Decide on parameter configuration
   - Sketch block template

3. **Create first test shader**
   - Simple color-changing shader
   - Verify end-to-end pipeline works

### Medium Term (Priority: 🟡 Low)
1. **Implement core shaders**
   - Noise, wave, particle effects
   - Document parameters

2. **Performance testing**
   - Profile with DevTools
   - Optimize as needed

### Long Term (Priority: ⚪ Maintenance)
1. **Final documentation**
2. **Cross-browser testing**
3. **Demo page creation**

---

## F. Progress Log

### Session 1 - 2026-05-22
**Status:** Plan created  
**Time:** 0.5 hours  
**Completed:**
- ✅ Researched Three.js, GLSL, Wagtail integration
- ✅ Created comprehensive implementation plan
- ✅ Defined 6-stage implementation roadmap
- ✅ Created checklist and timeline

**Notes:**
- Decided to start with Stage 1 (Foundation & Setup) next session
- Three.js will be integrated via static files for now
- Will use vanilla JavaScript for shader management (not TypeScript initially)
- Consider TSL (Three Shading Language) for future WebGPU compatibility

**Next Session:**
- Start Stage 1: Create directory structure and download Three.js
- Target: Get base shader manager operational

---

## 📚 References & Resources

### Official Documentation
- [Wagtail Documentation - StreamField](https://docs.wagtail.org/en/stable/topics/streamfield.html)
- [Wagtail - Custom StreamField Blocks](https://docs.wagtail.org/en/stable/advanced_topics/customization/streamfield_blocks.html)
- [Django Static Files](https://www.w3schools.com/django/django_add_static_files.html)
- [Three.js - Official Shaders Guide](https://threejs-journey.com/lessons/shaders)

### Shader Learning Resources
- [GLSL and Shaders Tutorial for Beginners](https://waelyasmina.net/articles/glsl-and-shaders-tutorial-for-beginners-webgl-threejs/)
- [An Introduction to Shaders - Part 1](https://aerotwist.com/tutorials/an-introduction-to-shaders-part-1/)
- [Using WebGL Shadertoy Shaders in Three.js](https://felixrieseberg.com/using-webgl-shadertoy-shaders-in-three-js/)

### Modern Shader Approaches
- [Three.js Shading Language (TSL) and WebGPU](https://blog.maximeheckel.com/posts/field-guide-to-tsl-and-webgpu/)
- [TSL: A New Era for Shaders](https://medium.com/@gianluca.lomarco/three-js-shading-language-cd48de8b22b0)

### Three.js Examples
- [Three.js Examples Repository](https://threejs.org/examples/)
- [WebGPU Renderer Guide](https://sbcode.net/threejs/webgpu-renderer/)

---

## 🛠️ Technical Notes

### Shader Architecture Decisions
1. **GLSL over TSL (for now)**
   - GLSL is more widely understood and documented
   - Can migrate to TSL later for WebGPU support
   - Maintains compatibility with older browsers

2. **File Organization**
   ```
   wagtaildevsite/
   ├── static/
   │   ├── js/
   │   │   ├── vendors/three.js (or CDN)
   │   │   ├── shader-manager.js
   │   │   └── shaders/
   │   │       ├── noise-shader.js
   │   │       ├── wave-shader.js
   │   │       └── particle-shader.js
   │   └── glsl/
   │       ├── noise.vertex.glsl
   │       ├── noise.fragment.glsl
   │       ├── wave.vertex.glsl
   │       ├── wave.fragment.glsl
   │       └── ... (more shaders)
   └── templates/
       └── blocks/
           └── shader_block.html
   ```

3. **Performance Considerations**
   - Limit to 1-2 active shaders per page initially
   - Use RequestAnimationFrame for rendering loop
   - Implement shader pooling if using multiple instances

### Browser Compatibility
- **Target:** Chrome 90+, Firefox 88+, Safari 14+
- **Fallback:** Display static image or message for WebGL-unsupported browsers
- **Mobile:** Test on iOS Safari and Chrome Mobile

---

**Document Version:** 1.0  
**Created:** 2026-05-22  
**Last Updated:** 2026-05-22
