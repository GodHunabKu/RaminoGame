<style>
.discord-page-modern {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.discord-hero {
    background: linear-gradient(135deg, #5865F2 0%, #7289DA 100%);
    border-radius: 25px;
    padding: 60px 40px;
    margin-bottom: 40px;
    box-shadow: 0 15px 50px rgba(88, 101, 242, 0.4);
    position: relative;
    overflow: hidden;
    text-align: center;
}

.discord-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.discord-hero-content {
    position: relative;
    z-index: 1;
}

.discord-logo {
    width: 120px;
    height: 120px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 25px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    animation: pulse-discord 3s ease-in-out infinite;
}

@keyframes pulse-discord {
    0%, 100% { transform: scale(1); box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3); }
    50% { transform: scale(1.05); box-shadow: 0 15px 60px rgba(0, 0, 0, 0.5); }
}

.discord-logo i {
    font-size: 60px;
    color: #fff;
}

.discord-hero h1 {
    font-size: 3rem;
    font-weight: 800;
    color: #fff;
    margin: 0 0 15px 0;
    text-transform: uppercase;
    letter-spacing: 2px;
    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.discord-hero p {
    font-size: 1.3rem;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
    font-weight: 500;
}

.discord-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    margin-bottom: 40px;
}

.discord-info-card {
    background: linear-gradient(135deg, rgba(88, 101, 242, 0.1) 0%, rgba(114, 137, 218, 0.05) 100%);
    border: 2px solid rgba(88, 101, 242, 0.3);
    border-radius: 20px;
    padding: 35px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.discord-info-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(88, 101, 242, 0.1), rgba(114, 137, 218, 0.1));
    opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
}

.discord-info-card:hover::before {
    opacity: 1;
}

.discord-info-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 60px rgba(88, 101, 242, 0.4);
    border-color: #5865F2;
}

.info-card-icon {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, #5865F2 0%, #7289DA 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(88, 101, 242, 0.4);
}

.info-card-icon i {
    font-size: 35px;
    color: #fff;
}

.discord-info-card h3 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
    margin: 0 0 15px 0;
}

.discord-info-card p {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.7;
    margin: 0;
}

.discord-widget-section {
    background: linear-gradient(135deg, rgba(26, 26, 46, 0.6) 0%, rgba(22, 33, 62, 0.6) 100%);
    border: 2px solid rgba(88, 101, 242, 0.3);
    border-radius: 25px;
    padding: 40px;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    overflow: hidden;
}

.discord-widget-section::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #5865F2, #7289DA, #5865F2, #7289DA);
    background-size: 300% 300%;
    border-radius: 25px;
    z-index: -1;
    animation: gradient-border 5s ease infinite;
    opacity: 0.5;
}

@keyframes gradient-border {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.widget-header {
    text-align: center;
    margin-bottom: 30px;
}

.widget-header h2 {
    font-size: 2rem;
    font-weight: 700;
    color: #fff;
    margin: 0 0 10px 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.widget-header h2 i {
    color: #5865F2;
    font-size: 2.2rem;
}

.widget-header p {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
}

.discord-widget-frame {
    width: 100%;
    max-width: 500px;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
    background: #2c2f33;
}

.discord-widget-frame iframe {
    display: block;
    width: 100%;
    height: 600px;
    border: none;
}

.discord-features {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
    margin-top: 40px;
}

.feature-box {
    background: rgba(88, 101, 242, 0.1);
    border: 1px solid rgba(88, 101, 242, 0.3);
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    transition: all 0.3s;
}

.feature-box:hover {
    background: rgba(88, 101, 242, 0.2);
    border-color: #5865F2;
    transform: translateY(-5px);
}

.feature-box i {
    font-size: 2.5rem;
    color: #5865F2;
    margin-bottom: 15px;
    display: block;
}

.feature-box h4 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #fff;
    margin: 0 0 10px 0;
}

.feature-box p {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
}

/* Responsive Design */
@media (max-width: 1024px) {
    .discord-content {
        grid-template-columns: 1fr;
        gap: 30px;
    }

    .discord-features {
        grid-template-columns: 1fr;
        gap: 20px;
    }
}

@media (max-width: 768px) {
    .discord-hero {
        padding: 40px 25px;
    }

    .discord-hero h1 {
        font-size: 2rem;
    }

    .discord-hero p {
        font-size: 1.1rem;
    }

    .discord-logo {
        width: 90px;
        height: 90px;
    }

    .discord-logo i {
        font-size: 45px;
    }

    .discord-info-card {
        padding: 25px;
    }

    .discord-widget-section {
        padding: 30px 20px;
    }

    .widget-header h2 {
        font-size: 1.6rem;
        flex-direction: column;
        gap: 10px;
    }

    .discord-widget-frame iframe {
        height: 500px;
    }
}

@media (max-width: 480px) {
    .discord-page-modern {
        padding: 15px;
    }

    .discord-hero {
        padding: 30px 20px;
    }

    .discord-hero h1 {
        font-size: 1.6rem;
        letter-spacing: 1px;
    }

    .discord-hero p {
        font-size: 1rem;
    }

    .discord-logo {
        width: 70px;
        height: 70px;
    }

    .discord-logo i {
        font-size: 35px;
    }

    .discord-info-card {
        padding: 20px;
    }

    .info-card-icon {
        width: 60px;
        height: 60px;
    }

    .info-card-icon i {
        font-size: 28px;
    }

    .discord-info-card h3 {
        font-size: 1.2rem;
    }

    .widget-header h2 {
        font-size: 1.4rem;
    }

    .discord-widget-frame iframe {
        height: 450px;
    }

    .feature-box {
        padding: 20px;
    }

    .feature-box i {
        font-size: 2rem;
    }
}
</style>

<div class="discord-page-modern">
    <!-- Hero Section -->
    <div class="discord-hero">
        <div class="discord-hero-content">
            <div class="discord-logo">
                <i class="fab fa-discord"></i>
            </div>
            <h1>Unisciti alla Community</h1>
            <p>Entra nel nostro server Discord ufficiale e chatta con altri giocatori!</p>
        </div>
    </div>

    <!-- Info Cards -->
    <div class="discord-content">
        <div class="discord-info-card">
            <div class="info-card-icon">
                <i class="fas fa-users"></i>
            </div>
            <h3>Community Attiva</h3>
            <p>Unisciti a centinaia di giocatori appassionati di Metin2. Condividi strategie, fai nuove amicizie e partecipa alle discussioni della community.</p>
        </div>

        <div class="discord-info-card">
            <div class="info-card-icon">
                <i class="fas fa-headset"></i>
            </div>
            <h3>Supporto in Tempo Reale</h3>
            <p>Hai bisogno di aiuto? Il nostro staff è sempre disponibile per rispondere alle tue domande e risolvere eventuali problemi rapidamente.</p>
        </div>

        <div class="discord-info-card">
            <div class="info-card-icon">
                <i class="fas fa-calendar-alt"></i>
            </div>
            <h3>Eventi Esclusivi</h3>
            <p>Partecipa agli eventi esclusivi, tornei e giveaway riservati ai membri del server Discord. Vinci premi incredibili!</p>
        </div>

        <div class="discord-info-card">
            <div class="info-card-icon">
                <i class="fas fa-bullhorn"></i>
            </div>
            <h3>Aggiornamenti Istantanei</h3>
            <p>Ricevi notifiche immediate su manutenzioni, update del server, nuove funzionalità e annunci importanti direttamente su Discord.</p>
        </div>
    </div>

    <!-- Discord Widget -->
    <div class="discord-widget-section">
        <div class="widget-header">
            <h2>
                <i class="fab fa-discord"></i>
                <span>Server Discord ONE</span>
            </h2>
            <p>Clicca sul widget qui sotto per unirti immediatamente</p>
        </div>

        <div class="discord-widget-frame">
            <iframe
                src="https://discord.com/widget?id=824954226114560001&theme=dark"
                allowtransparency="true"
                frameborder="0"
                sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts">
            </iframe>
        </div>
    </div>

    <!-- Features -->
    <div class="discord-features">
        <div class="feature-box">
            <i class="fas fa-comments"></i>
            <h4>Chat Vocale</h4>
            <p>Canali vocali dedicati per giocare insieme</p>
        </div>

        <div class="feature-box">
            <i class="fas fa-trophy"></i>
            <h4>Classifiche</h4>
            <p>Scopri i migliori giocatori del server</p>
        </div>

        <div class="feature-box">
            <i class="fas fa-gift"></i>
            <h4>Giveaway</h4>
            <p>Premi e bonus esclusivi per i membri</p>
        </div>
    </div>
</div>
