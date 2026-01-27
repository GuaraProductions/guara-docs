/**
 * Excalidraw SVG Pan and Zoom Library
 * Lightweight vanilla JavaScript implementation for static sites
 * No external dependencies required
 */

(function() {
  'use strict';

  // Store instances of pan/zoom controllers
  const instances = new Map();

  /**
   * Initialize pan and zoom for an Excalidraw SVG container
   */
  window.initExcalidrawPanZoom = function(containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error('Container not found:', containerId);
      return;
    }

    // Skip if already initialized
    if (instances.has(containerId)) {
      return;
    }

    const instance = {
      container: container,
      scale: 1,
      minScale: 0.1,
      maxScale: 10,
      translateX: 0,
      translateY: 0,
      isPanning: false,
      startX: 0,
      startY: 0,
      svgElement: null
    };

    // Wait for SVG to load
    const objectElement = container.querySelector('object');
    if (objectElement) {
      objectElement.addEventListener('load', function() {
        try {
          const svgDoc = objectElement.contentDocument;
          if (svgDoc) {
            instance.svgElement = svgDoc.documentElement;
            setupTransform(instance);
          }
        } catch (e) {
          console.warn('Could not access SVG content, using container-based zoom');
          setupContainerTransform(instance);
        }
      });
    } else {
      setupContainerTransform(instance);
    }

    // Mouse wheel zoom
    container.addEventListener('wheel', function(e) {
      e.preventDefault();
      const delta = e.deltaY > 0 ? 0.9 : 1.1;
      zoom(instance, delta, e.clientX, e.clientY);
    }, { passive: false });

    // Touch events - combined handler for zoom and pan
    let lastTouchDistance = 0;
    let lastTouchX = 0;
    let lastTouchY = 0;
    
    container.addEventListener('touchstart', function(e) {
      if (e.touches.length === 2) {
        e.preventDefault();
        lastTouchDistance = getTouchDistance(e.touches);
      } else if (e.touches.length === 1) {
        lastTouchX = e.touches[0].clientX;
        lastTouchY = e.touches[0].clientY;
      }
    }, { passive: false });

    container.addEventListener('touchmove', function(e) {
      if (e.touches.length === 2) {
        // Pinch to zoom
        e.preventDefault();
        const currentDistance = getTouchDistance(e.touches);
        const delta = currentDistance / lastTouchDistance;
        const centerX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
        const centerY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
        zoom(instance, delta, centerX, centerY);
        lastTouchDistance = currentDistance;
      } else if (e.touches.length === 1) {
        // Pan with one finger
        e.preventDefault();
        const deltaX = e.touches[0].clientX - lastTouchX;
        const deltaY = e.touches[0].clientY - lastTouchY;
        instance.translateX += deltaX;
        instance.translateY += deltaY;
        applyTransform(instance);
        lastTouchX = e.touches[0].clientX;
        lastTouchY = e.touches[0].clientY;
      }
    }, { passive: false });

    // Panning with mouse
    container.addEventListener('mousedown', function(e) {
      if (e.button === 0) { // Left click only
        instance.isPanning = true;
        instance.startX = e.clientX - instance.translateX;
        instance.startY = e.clientY - instance.translateY;
        container.style.cursor = 'grabbing';
        e.preventDefault();
      }
    });

    document.addEventListener('mousemove', function(e) {
      if (instance.isPanning) {
        instance.translateX = e.clientX - instance.startX;
        instance.translateY = e.clientY - instance.startY;
        applyTransform(instance);
        e.preventDefault();
      }
    });

    document.addEventListener('mouseup', function(e) {
      if (instance.isPanning) {
        instance.isPanning = false;
        container.style.cursor = 'grab';
      }
    });

    instances.set(containerId, instance);
  };

  /**
   * Control zoom via buttons
   */
  window.excalidrawZoom = function(containerId, action) {
    const instance = instances.get(containerId);
    if (!instance) return;

    const rect = instance.container.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    switch (action) {
      case 'in':
        zoom(instance, 1.2, centerX, centerY);
        break;
      case 'out':
        zoom(instance, 0.8, centerX, centerY);
        break;
      case 'reset':
        instance.scale = 1;
        instance.translateX = 0;
        instance.translateY = 0;
        applyTransform(instance);
        break;
    }
  };

  /**
   * Zoom function with origin point
   */
  function zoom(instance, delta, originX, originY) {
    const newScale = Math.max(instance.minScale, Math.min(instance.maxScale, instance.scale * delta));
    
    if (newScale !== instance.scale) {
      const rect = instance.container.getBoundingClientRect();
      const offsetX = originX - rect.left;
      const offsetY = originY - rect.top;

      // Adjust translation to zoom towards the cursor/touch point
      instance.translateX = offsetX - (offsetX - instance.translateX) * (newScale / instance.scale);
      instance.translateY = offsetY - (offsetY - instance.translateY) * (newScale / instance.scale);
      instance.scale = newScale;

      applyTransform(instance);
    }
  }

  /**
   * Apply transform to SVG element
   */
  function setupTransform(instance) {
    if (instance.svgElement) {
      // Enable pointer events for better interaction
      instance.svgElement.style.pointerEvents = 'none';
    }
    applyTransform(instance);
  }

  /**
   * Setup transform for container-based approach
   */
  function setupContainerTransform(instance) {
    const objectElement = instance.container.querySelector('object, img');
    if (objectElement) {
      objectElement.style.transformOrigin = '0 0';
    }
    applyTransform(instance);
  }

  /**
   * Apply the current transform
   */
  function applyTransform(instance) {
    const objectElement = instance.container.querySelector('object, img');
    if (objectElement) {
      const transform = `translate(${instance.translateX}px, ${instance.translateY}px) scale(${instance.scale})`;
      objectElement.style.transform = transform;
    }
  }

  /**
   * Get distance between two touch points
   */
  function getTouchDistance(touches) {
    const dx = touches[0].clientX - touches[1].clientX;
    const dy = touches[0].clientY - touches[1].clientY;
    return Math.sqrt(dx * dx + dy * dy);
  }
})();
