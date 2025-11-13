/**
 * ==========================================
 * ONE SERVER - JavaScript Ottimizzato
 * Version: 2.4
 * ==========================================
 */

(function() {
    'use strict';
    
    // ===== UTILITY FUNCTIONS =====
    const Utils = {
        // Debounce per ottimizzare eventi ripetuti
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        
        // Throttle per limitare la frequenza di esecuzione
        throttle(func, limit) {
            let inThrottle;
            return function(...args) {
                if (!inThrottle) {
                    func.apply(this, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },
        
        // Animazione smooth per scroll
        smoothScroll(target, duration = 800) {
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
            const startPosition = window.pageYOffset;
            const distance = targetPosition - startPosition;
            let startTime = null;

            function animation(currentTime) {
                if (startTime === null) startTime = currentTime;
                const timeElapsed = currentTime - startTime;
                const run = ease(timeElapsed, startPosition, distance, duration);
                window.scrollTo(0, run);
                if (timeElapsed < duration) requestAnimationFrame(animation);
            }

            function ease(t, b, c, d) {
                t /= d / 2;
                if (t < 1) return c / 2 * t * t + b;
                t--;
                return -c / 2 * (t * (t - 2) - 1) + b;
            }

            requestAnimationFrame(animation);
        }
    };

    // ===== PRELOADER =====
    const PreloaderModule = {
        init() {
            const preloader = document.getElementById('preloader');
            if (!preloader) return;

            // Nasconde il preloader quando la pagina è completamente caricata
            window.addEventListener('load', () => {
                setTimeout(() => {
                    preloader.classList.add('loaded');
                    document.body.classList.add('loaded');
                    
                    // Rimuove completamente il preloader dopo l'animazione
                    setTimeout(() => {
                        preloader.style.display = 'none';
                    }, 500);
                }, 300);
            });

            // Fallback: nasconde dopo 5 secondi anche se la pagina non ha finito di caricare
            setTimeout(() => {
                if (!preloader.classList.contains('loaded')) {
                    preloader.classList.add('loaded');
                    document.body.classList.add('loaded');
                }
            }, 5000);
        }
    };

    // ===== MOBILE MENU =====
    const MobileMenuModule = {
        init() {
            const mobileMenuButton = document.getElementById('mobile-menu-toggle');
            const sidebar = document.querySelector('.sidebar');
            
            if (!mobileMenuButton || !sidebar) return;

            // Toggle menu
            mobileMenuButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleMenu();
            });

            // Chiudi menu al click fuori
            document.addEventListener('click', (e) => {
                if (document.body.classList.contains('sidebar-open')) {
                    if (!sidebar.contains(e.target) && !mobileMenuButton.contains(e.target)) {
                        this.closeMenu();
                    }
                }
            });

            // Chiudi menu con ESC
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && document.body.classList.contains('sidebar-open')) {
                    this.closeMenu();
                }
            });

            // Chiudi menu al click su un link
            sidebar.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', () => {
                    this.closeMenu();
                });
            });
        },

        toggleMenu() {
            document.body.classList.toggle('sidebar-open');
            const isOpen = document.body.classList.contains('sidebar-open');
            
            // Previeni scroll del body quando il menu è aperto
            if (isOpen) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        },

        closeMenu() {
            document.body.classList.remove('sidebar-open');
            document.body.style.overflow = '';
        }
    };

    // ===== SMOOTH SCROLL =====
    const SmoothScrollModule = {
        init() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    const href = this.getAttribute('href');
                    
                    // Ignora link vuoti o solo "#"
                    if (!href || href === '#') return;
                    
                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        Utils.smoothScroll(target);
                    }
                });
            });
        }
    };

    // ===== PASSWORD STRENGTH INDICATOR =====
    const PasswordStrengthModule = {
        init() {
            const passwordInput = document.getElementById('password');
            const strengthFill = document.getElementById('strength-fill');
            const strengthText = document.getElementById('strength-text');
            
            if (!passwordInput || !strengthFill || !strengthText) return;

            passwordInput.addEventListener('input', () => {
                const password = passwordInput.value;
                const strength = this.calculateStrength(password);
                
                strengthFill.style.width = strength.percentage + '%';
                strengthText.textContent = strength.text;
                strengthText.style.color = strength.color;
            });
        },

        calculateStrength(password) {
            let score = 0;
            
            if (password.length === 0) {
                return { percentage: 0, text: 'Forza password', color: 'var(--color-text-dark)' };
            }
            
            // Lunghezza
            if (password.length >= 5) score += 25;
            if (password.length >= 8) score += 25;
            
            // Maiuscole
            if (/[A-Z]/.test(password)) score += 25;
            
            // Numeri
            if (/[0-9]/.test(password)) score += 25;
            
            // Caratteri speciali (bonus)
            if (/[^A-Za-z0-9]/.test(password)) score = Math.min(100, score + 10);
            
            // Determina testo e colore
            let text, color;
            if (score <= 25) {
                text = 'Debole';
                color = '#E74C3C';
            } else if (score <= 50) {
                text = 'Media';
                color = '#F39C12';
            } else if (score <= 75) {
                text = 'Buona';
                color = '#3498DB';
            } else {
                text = 'Forte';
                color = '#27AE60';
            }
            
            return { percentage: score, text, color };
        }
    };

    // ===== FORM VALIDATION =====
    const FormValidationModule = {
        init() {
            this.validateUsername();
            this.validateEmail();
            this.validatePasswordMatch();
        },

        validateUsername() {
            const usernameInput = document.getElementById('username');
            const checkNameEl = document.getElementById('checkname');
            const checkName2El = document.getElementById('checkname2');
            
            if (!usernameInput) return;

            usernameInput.addEventListener('input', Utils.debounce(() => {
                const username = usernameInput.value;
                
                // Reset messaggi
                if (checkNameEl) checkNameEl.textContent = '';
                if (checkName2El) checkName2El.textContent = '';
                
                // Validazione lunghezza
                if (username.length > 0 && username.length < 5) {
                    if (checkNameEl) checkNameEl.textContent = 'Username troppo corto (minimo 5 caratteri)';
                    return;
                }
                
                // Validazione caratteri
                if (username.length > 0 && !/^[A-Za-z0-9]+$/.test(username)) {
                    if (checkName2El) checkName2El.textContent = 'Solo lettere e numeri permessi';
                    return;
                }
                
                // Verifica disponibilità (se esiste l'endpoint)
                if (username.length >= 5 && typeof site_url !== 'undefined') {
                    this.checkUsernameAvailability(username, checkNameEl);
                }
            }, 500));
        },

        validateEmail() {
            const emailInput = document.getElementById('email');
            const checkEmailEl = document.getElementById('checkemail');
            
            if (!emailInput) return;

            emailInput.addEventListener('input', Utils.debounce(() => {
                const email = emailInput.value;
                
                if (checkEmailEl) checkEmailEl.textContent = '';
                
                if (email.length > 0 && !this.isValidEmail(email)) {
                    if (checkEmailEl) checkEmailEl.textContent = 'Indirizzo email non valido';
                }
            }, 500));
        },

        validatePasswordMatch() {
            const passwordInput = document.getElementById('password');
            const rpasswordInput = document.getElementById('rpassword');
            const checkPasswordEl = document.getElementById('checkpassword');
            
            if (!passwordInput || !rpasswordInput) return;

            rpasswordInput.addEventListener('input', () => {
                if (checkPasswordEl) checkPasswordEl.textContent = '';
                
                if (rpasswordInput.value.length > 0 && 
                    passwordInput.value !== rpasswordInput.value) {
                    if (checkPasswordEl) checkPasswordEl.textContent = 'Le password non coincidono';
                }
            });
        },

        isValidEmail(email) {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        },

        checkUsernameAvailability(username, element) {
            // Implementa chiamata AJAX per verificare disponibilità username
            // Esempio base (modifica secondo il tuo backend):
            /*
            fetch(`${site_url}api/check-username.php?username=${encodeURIComponent(username)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.available === false) {
                        element.textContent = 'Username già in uso';
                    } else {
                        element.textContent = '';
                        element.style.color = '#27AE60';
                        element.innerHTML = '<i class="fas fa-check"></i> Username disponibile';
                    }
                })
                .catch(error => console.error('Error:', error));
            */
        }
    };

    // ===== LAZY LOADING IMAGES =====
    const LazyLoadModule = {
        init() {
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries, observer) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            if (img.dataset.src) {
                                img.src = img.dataset.src;
                                img.removeAttribute('data-src');
                                img.classList.add('loaded');
                                observer.unobserve(img);
                            }
                        }
                    });
                });

                document.querySelectorAll('img[data-src]').forEach(img => {
                    imageObserver.observe(img);
                });
            } else {
                // Fallback per browser che non supportano IntersectionObserver
                document.querySelectorAll('img[data-src]').forEach(img => {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                });
            }
        }
    };

    // ===== ANIMATIONS ON SCROLL =====
    const ScrollAnimationsModule = {
        init() {
            if ('IntersectionObserver' in window) {
                const animationObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('animate-in');
                        }
                    });
                }, {
                    threshold: 0.1,
                    rootMargin: '0px 0px -50px 0px'
                });

                document.querySelectorAll('.content-box, .stat-box, .ranking-box').forEach(el => {
                    animationObserver.observe(el);
                });
            }
        }
    };

    // ===== BACK TO TOP BUTTON =====
    const BackToTopModule = {
        init() {
            // Crea il bottone se non esiste
            if (!document.getElementById('back-to-top')) {
                const button = document.createElement('button');
                button.id = 'back-to-top';
                button.innerHTML = '<i class="fas fa-arrow-up"></i>';
                button.setAttribute('aria-label', 'Torna su');
                document.body.appendChild(button);
                
                this.addStyles();
            }

            const backToTopButton = document.getElementById('back-to-top');
            if (!backToTopButton) return;

            // Mostra/nascondi bottone durante lo scroll
            window.addEventListener('scroll', Utils.throttle(() => {
                if (window.pageYOffset > 300) {
                    backToTopButton.classList.add('visible');
                } else {
                    backToTopButton.classList.remove('visible');
                }
            }, 200));

            // Click per tornare su
            backToTopButton.addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        },

        addStyles() {
            const style = document.createElement('style');
            style.textContent = `
                #back-to-top {
                    position: fixed;
                    bottom: 30px;
                    right: 30px;
                    width: 50px;
                    height: 50px;
                    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
                    border: none;
                    border-radius: 50%;
                    color: white;
                    font-size: 20px;
                    cursor: pointer;
                    opacity: 0;
                    visibility: hidden;
                    transform: translateY(20px);
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
                    z-index: 999;
                }
                #back-to-top.visible {
                    opacity: 1;
                    visibility: visible;
                    transform: translateY(0);
                }
                #back-to-top:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 8px 25px rgba(231, 76, 60, 0.5);
                }
                @media (max-width: 768px) {
                    #back-to-top {
                        bottom: 20px;
                        right: 20px;
                        width: 45px;
                        height: 45px;
                        font-size: 18px;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    };

    // ===== DROPDOWN MENU =====
    const DropdownModule = {
        init() {
            const dropdowns = document.querySelectorAll('.dropdown');
            
            dropdowns.forEach(dropdown => {
                const button = dropdown.querySelector('.dropbtn');
                const content = dropdown.querySelector('.dropdown-content');
                
                if (!button || !content) return;

                // Toggle on click
                button.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.closeAllDropdowns();
                    dropdown.classList.toggle('active');
                });

                // Chiudi al click fuori
                document.addEventListener('click', () => {
                    dropdown.classList.remove('active');
                });
            });
        },

        closeAllDropdowns() {
            document.querySelectorAll('.dropdown.active').forEach(d => {
                d.classList.remove('active');
            });
        }
    };

    // ===== FAQ ACCORDION =====
    const FAQModule = {
        init() {
            const faqItems = document.querySelectorAll('.faq-item');
            
            faqItems.forEach(item => {
                const question = item.querySelector('.faq-question');
                const answer = item.querySelector('.faq-answer');
                
                if (!question || !answer) return;

                question.addEventListener('click', () => {
                    const isActive = item.classList.contains('active');
                    
                    // Chiudi tutti gli altri
                    faqItems.forEach(i => i.classList.remove('active'));
                    
                    // Toggle corrente
                    if (!isActive) {
                        item.classList.add('active');
                    }
                });
            });
        }
    };

    // ===== CONSOLE ART =====
    const ConsoleArtModule = {
        init() {
            const styles = [
                'color: #E74C3C',
                'font-size: 20px',
                'font-weight: bold',
                'text-shadow: 2px 2px 0px #C0392B'
            ].join(';');

            console.log('%c?? ONE SERVER ??', styles);
            console.log('%cSito caricato con successo!', 'color: #27AE60; font-size: 14px;');
            console.log('%cVersion: 2.4 - Ottimizzato', 'color: #95A5A6; font-size: 12px;');
            
            // Easter egg
            console.log('%cCurioso? Unisciti al nostro team! ??', 'color: #3498DB; font-size: 12px;');
        }
    };

    // ===== PERFORMANCE MONITORING =====
    const PerformanceModule = {
        init() {
            if ('performance' in window) {
                window.addEventListener('load', () => {
                    setTimeout(() => {
                        const perfData = performance.timing;
                        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                        const connectTime = perfData.responseEnd - perfData.requestStart;
                        
                        console.log(`? Page Load Time: ${pageLoadTime}ms`);
                        console.log(`?? Server Response: ${connectTime}ms`);
                    }, 0);
                });
            }
        }
    };

    // ===== MAIN INITIALIZATION =====
    document.addEventListener('DOMContentLoaded', () => {
        try {
            PreloaderModule.init();
            MobileMenuModule.init();
            SmoothScrollModule.init();
            PasswordStrengthModule.init();
            FormValidationModule.init();
            LazyLoadModule.init();
            ScrollAnimationsModule.init();
            BackToTopModule.init();
            DropdownModule.init();
            FAQModule.init();
            ConsoleArtModule.init();
            PerformanceModule.init();
        } catch (error) {
            console.error('Errore durante l\'inizializzazione:', error);
        }
    });

})();