/**
 * ADMINISTRATION V2 - JavaScript Dedicato
 * Gestione interazioni e animazioni per la pagina account
 */

(function() {
    'use strict';

    // Auto-hide notification dopo 5 secondi
    function initNotifications() {
        const notification = document.getElementById('mainNotification');
        if (notification) {
            setTimeout(function() {
                notification.style.animation = 'slideOutUp 0.5s ease';
                setTimeout(function() {
                    notification.remove();
                }, 500);
            }, 5000);
        }
    }

    // Animazione di entrata per le card - DISABILITATA
    function initCardAnimations() {
        // Animazioni disabilitate - elementi appaiono immediatamente
        return;
    }

    // Conferma per azioni critiche
    function initFormConfirmations() {
        const forms = document.querySelectorAll('.action-item form');

        forms.forEach(function(form) {
            form.addEventListener('submit', function(e) {
                const button = form.querySelector('button[type="submit"]');
                if (button) {
                    // Disabilita il pulsante per evitare doppio click
                    button.disabled = true;
                    button.style.opacity = '0.6';
                    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Invio...';

                    // Se l'utente annulla la conferma, riabilita il pulsante
                    setTimeout(function() {
                        if (!confirm('Sei sicuro di voler procedere?')) {
                            button.disabled = false;
                            button.style.opacity = '1';
                            // Ripristina il contenuto originale
                            const originalText = button.getAttribute('data-original-text');
                            if (originalText) {
                                button.innerHTML = originalText;
                            }
                        }
                    }, 100);
                }
            });

            // Salva il testo originale del pulsante
            const button = form.querySelector('button[type="submit"]');
            if (button) {
                button.setAttribute('data-original-text', button.innerHTML);
            }
        });
    }

    // Effetto particelle al click sui pulsanti
    function createClickEffect(e) {
        const ripple = document.createElement('span');
        ripple.style.position = 'absolute';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(255, 255, 255, 0.6)';
        ripple.style.width = '20px';
        ripple.style.height = '20px';
        ripple.style.left = e.offsetX + 'px';
        ripple.style.top = e.offsetY + 'px';
        ripple.style.transform = 'translate(-50%, -50%)';
        ripple.style.pointerEvents = 'none';
        ripple.style.animation = 'rippleEffect 0.6s ease-out';

        this.appendChild(ripple);

        setTimeout(function() {
            ripple.remove();
        }, 600);
    }

    function initButtonEffects() {
        const buttons = document.querySelectorAll('.action-btn');
        buttons.forEach(function(btn) {
            btn.style.position = 'relative';
            btn.style.overflow = 'hidden';
            btn.addEventListener('click', createClickEffect);
        });

        // Aggiungi CSS per l'animazione ripple
        if (!document.getElementById('rippleAnimation')) {
            const style = document.createElement('style');
            style.id = 'rippleAnimation';
            style.textContent = `
                @keyframes rippleEffect {
                    from {
                        transform: translate(-50%, -50%) scale(0);
                        opacity: 1;
                    }
                    to {
                        transform: translate(-50%, -50%) scale(4);
                        opacity: 0;
                    }
                }

                @keyframes slideOutUp {
                    from {
                        opacity: 1;
                        transform: translateY(0);
                    }
                    to {
                        opacity: 0;
                        transform: translateY(-20px);
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // Scroll smooth per la pagina
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Inizializza tutto quando il DOM è pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        initNotifications();
        initCardAnimations();
        initButtonEffects();
        initSmoothScroll();
    }
})();
