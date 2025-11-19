/**
 * MODERN FEATURES 2025
 * Toast Notifications, Loading States, Animations
 */

(function() {
    'use strict';

    // ==================== TOAST NOTIFICATIONS ====================
    const ToastManager = {
        container: null,

        init: function() {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        },

        show: function(message, type = 'info', duration = 3000) {
            const toast = document.createElement('div');
            toast.className = `toast toast-${type} animate-slideInRight`;

            const icon = this.getIcon(type);
            toast.innerHTML = `
                <span style="font-size: 1.25rem;">${icon}</span>
                <span style="flex: 1; color: var(--text-primary);">${message}</span>
                <button onclick="this.parentElement.remove()" style="background: none; border: none; color: var(--text-secondary); cursor: pointer; font-size: 1.25rem; padding: 0; margin-left: var(--space-2);" aria-label="Close">×</button>
            `;

            this.container.appendChild(toast);

            // Auto remove after duration
            setTimeout(() => {
                toast.remove();
            }, duration);

            return toast;
        },

        getIcon: function(type) {
            const icons = {
                success: '✓',
                error: '✕',
                warning: '⚠',
                info: 'ℹ'
            };
            return icons[type] || icons.info;
        },

        success: function(message, duration) {
            return this.show(message, 'success', duration);
        },

        error: function(message, duration) {
            return this.show(message, 'error', duration);
        },

        warning: function(message, duration) {
            return this.show(message, 'warning', duration);
        },

        info: function(message, duration) {
            return this.show(message, 'info', duration);
        }
    };

    // ==================== LOADING STATES ====================
    const LoadingManager = {
        // Add loading state to button
        addToButton: function(button) {
            if (!button) return;

            button.classList.add('btn-loading');
            button.setAttribute('disabled', 'disabled');
            button.dataset.originalText = button.textContent;
        },

        // Remove loading state from button
        removeFromButton: function(button) {
            if (!button) return;

            button.classList.remove('btn-loading');
            button.removeAttribute('disabled');
            if (button.dataset.originalText) {
                button.textContent = button.dataset.originalText;
            }
        },

        // Show full page loader
        showPageLoader: function() {
            let loader = document.getElementById('page-loader');
            if (!loader) {
                loader = document.createElement('div');
                loader.id = 'page-loader';
                loader.innerHTML = '<div class="spinner"></div>';
                loader.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 9999; pointer-events: auto;';
                document.body.appendChild(loader);
            }
            loader.style.display = 'flex';
            loader.style.pointerEvents = 'auto';
        },

        // Hide full page loader
        hidePageLoader: function() {
            const loader = document.getElementById('page-loader');
            if (loader) {
                loader.style.display = 'none';
                loader.style.pointerEvents = 'none';  // FIX: Non blocca più i click quando nascosto
            }
        }
    };

    // ==================== SMOOTH SCROLL ====================
    const SmoothScroll = {
        init: function() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    const href = this.getAttribute('href');
                    if (href === '#') return;

                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        }
    };

    // ==================== FORM ENHANCEMENTS ====================
    const FormEnhancer = {
        init: function() {
            // Add modern input classes
            document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], textarea, select').forEach(input => {
                if (!input.classList.contains('input-modern')) {
                    input.classList.add('input-modern');
                }
            });

            // Add modern button classes
            document.querySelectorAll('button[type="submit"], input[type="submit"]').forEach(button => {
                if (!button.classList.contains('btn-modern')) {
                    button.classList.add('btn-modern', 'btn-primary-modern');
                }
            });

            // Enhance AJAX forms with loading states
            this.enhanceAjaxForms();
        },

        enhanceAjaxForms: function() {
            document.querySelectorAll('form').forEach(form => {
                form.addEventListener('submit', function(e) {
                    const submitBtn = this.querySelector('button[type="submit"], input[type="submit"]');
                    if (submitBtn) {
                        LoadingManager.addToButton(submitBtn);

                        // Auto-remove loading state after 10 seconds as fallback
                        setTimeout(() => {
                            LoadingManager.removeFromButton(submitBtn);
                        }, 10000);
                    }
                });
            });
        }
    };

    // ==================== CARD ANIMATIONS ====================
    const CardAnimator = {
        init: function() {
            // Animazioni disabilitate - aggiunge solo card-modern senza animate-fadeIn
            document.querySelectorAll('.card, .panel, .box').forEach(card => {
                if (!card.classList.contains('card-modern')) {
                    card.classList.add('card-modern');
                    // Rimosso 'animate-fadeIn' per evitare animazioni fastidiose
                }
            });

            // IntersectionObserver disabilitato - gli elementi appaiono immediatamente
            return;
        }
    };

    // ==================== ACCESSIBILITY ====================
    const AccessibilityEnhancer = {
        init: function() {
            // Add focus-visible class to interactive elements
            document.querySelectorAll('button, a, input, select, textarea').forEach(el => {
                el.classList.add('focus-visible');
            });

            // Add ARIA labels where missing
            document.querySelectorAll('button:not([aria-label])').forEach(btn => {
                const text = btn.textContent.trim();
                if (text) {
                    btn.setAttribute('aria-label', text);
                }
            });

            // Add skip to main content link
            this.addSkipLink();
        },

        addSkipLink: function() {
            const main = document.querySelector('main, #main, .main-content');
            if (main && !main.id) {
                main.id = 'main-content';
            }

            if (main && !document.querySelector('.skip-to-main')) {
                const skipLink = document.createElement('a');
                skipLink.href = '#main-content';
                skipLink.className = 'skip-to-main sr-only focus-visible';
                skipLink.textContent = 'Skip to main content';
                skipLink.style.cssText = 'position: absolute; top: 0; left: 0; z-index: 99999;';
                skipLink.addEventListener('focus', function() {
                    this.classList.remove('sr-only');
                });
                skipLink.addEventListener('blur', function() {
                    this.classList.add('sr-only');
                });
                document.body.insertBefore(skipLink, document.body.firstChild);
            }
        }
    };

    // ==================== GLOBAL AJAX IMPROVEMENTS ====================
    const AjaxEnhancer = {
        init: function() {
            // Override jQuery AJAX to add automatic toast notifications
            if (window.jQuery) {
                const originalAjax = jQuery.ajax;
                jQuery.ajax = function(options) {
                    const originalSuccess = options.success;
                    const originalError = options.error;

                    // Wrap success handler
                    options.success = function(data, textStatus, jqXHR) {
                        if (originalSuccess) {
                            originalSuccess.apply(this, arguments);
                        }
                    };

                    // Wrap error handler
                    options.error = function(jqXHR, textStatus, errorThrown) {
                        if (originalError) {
                            originalError.apply(this, arguments);
                        } else {
                            // Show error toast if no custom error handler
                            ToastManager.error('Connection error. Please try again.');
                        }
                    };

                    return originalAjax.call(jQuery, options);
                };
            }
        }
    };

    // ==================== PERFORMANCE OPTIMIZER ====================
    const PerformanceOptimizer = {
        init: function() {
            // Lazy load images
            this.lazyLoadImages();

            // Debounce resize events
            this.optimizeResizeEvents();
        },

        lazyLoadImages: function() {
            const images = document.querySelectorAll('img[data-src]');

            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        },

        optimizeResizeEvents: function() {
            let resizeTimer;
            window.addEventListener('resize', function() {
                clearTimeout(resizeTimer);
                resizeTimer = setTimeout(function() {
                    window.dispatchEvent(new Event('optimizedResize'));
                }, 250);
            });
        }
    };

    // ==================== INITIALIZE ALL ====================
    function initModernFeatures() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }

        function init() {
            // console.log('🚀 Modern Features 2025 - Initializing...');

            ToastManager.init();
            SmoothScroll.init();
            FormEnhancer.init();
            CardAnimator.init();
            AccessibilityEnhancer.init();
            AjaxEnhancer.init();
            PerformanceOptimizer.init();

            // console.log('✓ Modern Features 2025 - Ready!');
        }
    }

    // Start initialization
    initModernFeatures();

    // Expose utilities globally
    window.ModernFeatures = {
        toast: ToastManager,
        loading: LoadingManager
    };

})();
