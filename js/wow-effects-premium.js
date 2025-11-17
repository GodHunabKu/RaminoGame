/**
 * ==========================================
 * EFFETTI WOW PREMIUM 2025 - ULTRA EPICI
 * Effetti che lasceranno a bocca aperta
 * ==========================================
 */

(function() {
    'use strict';

    // ==================== CONFIGURAZIONE WOW ====================
    const WOW_CONFIG = {
        cursorTrail: {
            enabled: true,
            particles: 8,
            colors: ['#FFD700', '#FFA500', '#FF6B6B', '#4ECDC4']
        },
        soundEffects: {
            enabled: false, // Disabilitato di default, attivabile da utente
            hoverVolume: 0.3,
            clickVolume: 0.5
        },
        easterEggs: {
            enabled: true,
            konamiCode: true,
            secretShortcuts: true
        },
        premiumEffects: {
            cursorGlow: true,
            magneticButtons: true,
            textReveal: true,
            scrollMagic: true
        }
    };

    // ==================== CURSOR TRAIL PREMIUM ====================
    class CursorTrail {
        constructor() {
            this.particles = [];
            this.mouse = { x: 0, y: 0 };
            this.init();
        }

        init() {
            if (!WOW_CONFIG.cursorTrail.enabled) return;
            if (window.innerWidth < 768) return; // Skip su mobile

            document.addEventListener('mousemove', (e) => {
                this.mouse.x = e.clientX;
                this.mouse.y = e.clientY;
                this.createParticle();
            });

            this.animate();
        }

        createParticle() {
            const particle = document.createElement('div');
            particle.className = 'cursor-trail-particle';

            const color = WOW_CONFIG.cursorTrail.colors[
                Math.floor(Math.random() * WOW_CONFIG.cursorTrail.colors.length)
            ];

            particle.style.cssText = `
                position: fixed;
                width: 8px;
                height: 8px;
                background: ${color};
                border-radius: 50%;
                pointer-events: none;
                z-index: 9998;
                left: ${this.mouse.x}px;
                top: ${this.mouse.y}px;
                opacity: 1;
                box-shadow: 0 0 10px ${color}, 0 0 20px ${color};
                animation: cursorTrailFade 0.8s ease-out forwards;
            `;

            document.body.appendChild(particle);

            setTimeout(() => particle.remove(), 800);
        }

        animate() {
            requestAnimationFrame(() => this.animate());
        }
    }

    // ==================== MAGNETIC BUTTONS ====================
    class MagneticButtons {
        constructor() {
            this.buttons = [];
            this.init();
        }

        init() {
            if (!WOW_CONFIG.premiumEffects.magneticButtons) return;

            const selectors = [
                '.cta-button',
                '.btn-submit',
                '.btn-download',
                '.itemshop-premium a',
                '.gold-premium-link'
            ];

            selectors.forEach(selector => {
                document.querySelectorAll(selector).forEach(btn => {
                    this.applyMagneticEffect(btn);
                });
            });
        }

        applyMagneticEffect(element) {
            element.addEventListener('mousemove', (e) => {
                const rect = element.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;

                const moveX = x * 0.3;
                const moveY = y * 0.3;

                element.style.transform = `translate(${moveX}px, ${moveY}px) scale(1.05)`;
            });

            element.addEventListener('mouseleave', () => {
                element.style.transform = 'translate(0, 0) scale(1)';
            });
        }
    }

    // ==================== TEXT REVEAL ANIMATION ====================
    class TextReveal {
        constructor() {
            this.init();
        }

        init() {
            if (!WOW_CONFIG.premiumEffects.textReveal) return;

            const selectors = [
                '.hero-tagline',
                '.content-box h3',
                '.stat-info h4'
            ];

            selectors.forEach(selector => {
                document.querySelectorAll(selector).forEach(el => {
                    this.wrapText(el);
                });
            });
        }

        wrapText(element) {
            const text = element.textContent;
            element.innerHTML = '';

            text.split('').forEach((char, index) => {
                const span = document.createElement('span');
                span.textContent = char === ' ' ? '\u00A0' : char;
                span.style.cssText = `
                    display: inline-block;
                    opacity: 0;
                    transform: translateY(20px);
                    animation: textRevealChar 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
                    animation-delay: ${index * 0.03}s;
                `;
                element.appendChild(span);
            });
        }
    }

    // ==================== EASTER EGGS ====================
    class EasterEggs {
        constructor() {
            this.konamiSequence = [];
            this.konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // ↑↑↓↓←→←→BA
            this.init();
        }

        init() {
            if (!WOW_CONFIG.easterEggs.enabled) return;

            // Konami Code
            if (WOW_CONFIG.easterEggs.konamiCode) {
                document.addEventListener('keydown', (e) => this.checkKonamiCode(e));
            }

            // Triple Click Logo
            const logo = document.querySelector('.hero-logo img');
            if (logo) {
                let clickCount = 0;
                logo.addEventListener('click', () => {
                    clickCount++;
                    if (clickCount === 3) {
                        this.activateRainbowMode();
                        clickCount = 0;
                    }
                    setTimeout(() => clickCount = 0, 1000);
                });
            }

            // Secret Shortcut: ALT + G = Gold Rain
            document.addEventListener('keydown', (e) => {
                if (e.altKey && e.key === 'g') {
                    this.goldRain();
                }
            });
        }

        checkKonamiCode(e) {
            this.konamiSequence.push(e.keyCode);
            this.konamiSequence = this.konamiSequence.slice(-10);

            if (this.konamiSequence.join(',') === this.konamiCode.join(',')) {
                this.activateSuperMode();
            }
        }

        activateSuperMode() {
            console.log('🎮 SUPER MODE ACTIVATED!');

            // Create notification
            this.showNotification('🎮 SUPER MODE ACTIVATED! 🚀', 'gold');

            // Increase particle count
            const particleSystem = window.premiumParticleSystem;
            if (particleSystem) {
                WOW_CONFIG.cursorTrail.particles = 20;
            }

            // Add rainbow glow to everything
            document.body.classList.add('super-mode');

            setTimeout(() => {
                document.body.classList.remove('super-mode');
                WOW_CONFIG.cursorTrail.particles = 8;
            }, 10000);
        }

        activateRainbowMode() {
            console.log('🌈 RAINBOW MODE!');
            this.showNotification('🌈 RAINBOW MODE! Grafica Premium Sbloccata!', 'rainbow');

            document.documentElement.style.setProperty('--gold-primary', 'hsl(0, 100%, 50%)');

            let hue = 0;
            const interval = setInterval(() => {
                hue = (hue + 2) % 360;
                document.documentElement.style.setProperty('--gold-primary', `hsl(${hue}, 100%, 50%)`);
            }, 50);

            setTimeout(() => {
                clearInterval(interval);
                document.documentElement.style.setProperty('--gold-primary', '#FFD700');
                this.showNotification('✨ Modalità normale ripristinata', 'info');
            }, 5000);
        }

        goldRain() {
            console.log('💰 GOLD RAIN!');
            this.showNotification('💰 GOLD RAIN! 💰', 'gold');

            for (let i = 0; i < 50; i++) {
                setTimeout(() => {
                    const coin = document.createElement('div');
                    coin.innerHTML = '💰';
                    coin.style.cssText = `
                        position: fixed;
                        left: ${Math.random() * 100}%;
                        top: -50px;
                        font-size: 40px;
                        pointer-events: none;
                        z-index: 9999;
                        animation: coinFall ${2 + Math.random() * 2}s linear forwards;
                    `;
                    document.body.appendChild(coin);
                    setTimeout(() => coin.remove(), 4000);
                }, i * 100);
            }
        }

        showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `wow-notification wow-notification-${type}`;
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 20px 30px;
                background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                color: #000;
                font-weight: 900;
                font-size: 16px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(255, 215, 0, 0.6);
                z-index: 10000;
                animation: notificationSlide 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            `;

            if (type === 'rainbow') {
                notification.style.background = 'linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #FFD700 100%)';
            }

            document.body.appendChild(notification);

            setTimeout(() => {
                notification.style.animation = 'notificationSlideOut 0.5s ease-out forwards';
                setTimeout(() => notification.remove(), 500);
            }, 3000);
        }
    }

    // ==================== SCROLL MAGIC ====================
    class ScrollMagic {
        constructor() {
            this.init();
        }

        init() {
            if (!WOW_CONFIG.premiumEffects.scrollMagic) return;

            let lastScroll = 0;
            let ticking = false;

            window.addEventListener('scroll', () => {
                lastScroll = window.scrollY;

                if (!ticking) {
                    window.requestAnimationFrame(() => {
                        this.updateParallax(lastScroll);
                        ticking = false;
                    });
                    ticking = true;
                }
            });
        }

        updateParallax(scrollY) {
            // Parallax su hero section
            const hero = document.querySelector('.hero-section');
            if (hero) {
                hero.style.transform = `translateY(${scrollY * 0.3}px)`;
                hero.style.opacity = 1 - (scrollY / 600);
            }

            // Floating elements
            document.querySelectorAll('.content-box').forEach((box, index) => {
                const speed = 0.05 + (index * 0.02);
                const y = (scrollY - box.offsetTop) * speed;
                box.style.transform = `translateY(${y}px)`;
            });
        }
    }

    // ==================== PERFORMANCE STATS (Dev Mode) ====================
    class PerformanceStats {
        constructor() {
            this.fps = 0;
            this.lastTime = performance.now();
            this.frameCount = 0;
        }

        init() {
            // Attiva solo con: localStorage.setItem('dev_mode', 'true')
            if (localStorage.getItem('dev_mode') !== 'true') return;

            this.createStatsDisplay();
            this.updateStats();
        }

        createStatsDisplay() {
            const stats = document.createElement('div');
            stats.id = 'performance-stats';
            stats.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: rgba(0, 0, 0, 0.8);
                color: #0F0;
                padding: 10px 15px;
                border-radius: 8px;
                font-family: monospace;
                font-size: 12px;
                z-index: 10001;
                border: 1px solid #0F0;
            `;
            document.body.appendChild(stats);
        }

        updateStats() {
            const now = performance.now();
            this.frameCount++;

            if (now >= this.lastTime + 1000) {
                this.fps = Math.round((this.frameCount * 1000) / (now - this.lastTime));
                this.frameCount = 0;
                this.lastTime = now;

                const stats = document.getElementById('performance-stats');
                if (stats) {
                    const memory = performance.memory ?
                        `${Math.round(performance.memory.usedJSHeapSize / 1048576)}MB` : 'N/A';

                    stats.innerHTML = `
                        FPS: ${this.fps}<br>
                        Memory: ${memory}<br>
                        Particles: ${document.querySelectorAll('.particle').length}
                    `;
                }
            }

            requestAnimationFrame(() => this.updateStats());
        }
    }

    // ==================== CURSOR GLOW ====================
    class CursorGlow {
        constructor() {
            this.cursor = null;
            this.init();
        }

        init() {
            if (!WOW_CONFIG.premiumEffects.cursorGlow) return;
            if (window.innerWidth < 768) return;

            this.cursor = document.createElement('div');
            this.cursor.className = 'cursor-glow';
            this.cursor.style.cssText = `
                position: fixed;
                width: 200px;
                height: 200px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(255, 215, 0, 0.15) 0%, transparent 70%);
                pointer-events: none;
                z-index: 9997;
                mix-blend-mode: screen;
                transition: transform 0.15s ease-out;
            `;

            document.body.appendChild(this.cursor);

            document.addEventListener('mousemove', (e) => {
                this.cursor.style.left = (e.clientX - 100) + 'px';
                this.cursor.style.top = (e.clientY - 100) + 'px';
            });
        }
    }

    // ==================== LOADING SCREEN PREMIUM ====================
    class LoadingScreen {
        constructor() {
            this.screen = null;
            this.init();
        }

        init() {
            this.createScreen();
            this.startLoading();
        }

        createScreen() {
            this.screen = document.createElement('div');
            this.screen.id = 'premium-loading-screen';
            this.screen.innerHTML = `
                <div class="loading-content">
                    <div class="loading-logo">
                        <div class="loading-spinner"></div>
                        <div class="loading-glow"></div>
                    </div>
                    <h2 class="loading-title">ONE SERVER</h2>
                    <p class="loading-subtitle">Caricamento esperienza premium...</p>
                    <div class="loading-bar">
                        <div class="loading-progress" id="loading-progress"></div>
                    </div>
                    <p class="loading-percentage" id="loading-percentage">0%</p>
                </div>
            `;

            this.screen.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
                z-index: 99999;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 1;
                transition: opacity 0.5s ease-out;
            `;

            document.body.appendChild(this.screen);
        }

        startLoading() {
            let progress = 0;
            const progressBar = document.getElementById('loading-progress');
            const percentage = document.getElementById('loading-percentage');

            const interval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                    setTimeout(() => this.hideScreen(), 500);
                }

                if (progressBar && percentage) {
                    progressBar.style.width = progress + '%';
                    percentage.textContent = Math.round(progress) + '%';
                }
            }, 200);
        }

        hideScreen() {
            if (this.screen) {
                this.screen.style.opacity = '0';
                setTimeout(() => {
                    this.screen.remove();
                    document.body.classList.add('loaded');
                }, 500);
            }
        }
    }

    // ==================== INITIALIZATION ====================
    function initWOWEffects() {
        console.log('✨ WOW Effects Premium 2025 - Initializing...');

        // Solo sulla homepage
        if (!document.querySelector('.hero-section')) return;

        // Loading Screen
        new LoadingScreen();

        // Cursor Effects
        setTimeout(() => {
            new CursorTrail();
            new CursorGlow();
        }, 1000);

        // Interactive Effects
        setTimeout(() => {
            new MagneticButtons();
            new TextReveal();
            new ScrollMagic();
        }, 1500);

        // Easter Eggs
        setTimeout(() => {
            new EasterEggs();
        }, 2000);

        // Performance Stats (dev mode)
        const perfStats = new PerformanceStats();
        perfStats.init();

        console.log('✅ WOW Effects Premium 2025 - Ready!');
        console.log('🎮 Easter Eggs Attivi:');
        console.log('   - Konami Code (↑↑↓↓←→←→BA) = Super Mode');
        console.log('   - Triple Click Logo = Rainbow Mode');
        console.log('   - ALT + G = Gold Rain');
        console.log('   - localStorage.setItem("dev_mode", "true") = Performance Stats');
    }

    // Start
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWOWEffects);
    } else {
        initWOWEffects();
    }

    // Add CSS animations
    if (!document.getElementById('wow-effects-styles')) {
        const style = document.createElement('style');
        style.id = 'wow-effects-styles';
        style.textContent = `
            @keyframes cursorTrailFade {
                to {
                    opacity: 0;
                    transform: scale(0) translateY(-30px);
                }
            }

            @keyframes textRevealChar {
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes notificationSlide {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            @keyframes notificationSlideOut {
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }

            @keyframes coinFall {
                to {
                    top: 100vh;
                    transform: rotate(720deg);
                }
            }

            .super-mode * {
                animation-duration: 0.3s !important;
            }

            .super-mode .hero-logo img {
                animation: superSpin 2s linear infinite !important;
            }

            @keyframes superSpin {
                to {
                    transform: rotate(360deg) scale(1.2);
                }
            }

            /* Loading Screen Styles */
            .loading-content {
                text-align: center;
                color: #FFD700;
            }

            .loading-logo {
                position: relative;
                width: 150px;
                height: 150px;
                margin: 0 auto 30px;
            }

            .loading-spinner {
                width: 150px;
                height: 150px;
                border: 4px solid rgba(255, 215, 0, 0.2);
                border-top-color: #FFD700;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }

            .loading-glow {
                position: absolute;
                top: 50%;
                left: 50%;
                width: 100px;
                height: 100px;
                margin: -50px 0 0 -50px;
                background: radial-gradient(circle, rgba(255, 215, 0, 0.3) 0%, transparent 70%);
                border-radius: 50%;
                animation: pulse 2s ease-in-out infinite;
            }

            .loading-title {
                font-family: 'Cinzel', serif;
                font-size: 48px;
                font-weight: 900;
                margin: 0 0 10px;
                background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .loading-subtitle {
                font-size: 16px;
                color: rgba(255, 215, 0, 0.7);
                margin: 0 0 30px;
            }

            .loading-bar {
                width: 300px;
                height: 6px;
                background: rgba(255, 215, 0, 0.2);
                border-radius: 3px;
                margin: 0 auto 15px;
                overflow: hidden;
            }

            .loading-progress {
                height: 100%;
                background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%);
                border-radius: 3px;
                width: 0;
                transition: width 0.3s ease-out;
                box-shadow: 0 0 10px #FFD700;
            }

            .loading-percentage {
                font-size: 18px;
                font-weight: 700;
                color: #FFD700;
                margin: 0;
            }
        `;
        document.head.appendChild(style);
    }

})();
