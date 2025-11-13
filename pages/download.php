<div class="download-page">
    <div class="download-hero">
        <div class="download-hero-content">
            <div class="hero-icon">
                <i class="fas fa-download"></i>
            </div>
            <h1 class="download-title">DOWNLOAD CLIENT</h1>
            <p class="download-subtitle">Scarica il client ufficiale e inizia la tua avventura!</p>
        </div>
    </div>

    <?php if(count($jsondataDownload)) { ?>
    <div class="download-grid">
        <?php $i=1; foreach($jsondataDownload as $key => $download) { ?>
        <div class="download-card">
            <div class="card-badge">
                <?php if($i == 1) { ?>
                <span class="badge-primary"><i class="fas fa-star"></i> Principale</span>
                <?php } else { ?>
                <span class="badge-mirror"><i class="fas fa-clone"></i> Mirror #<?php echo $i; ?></span>
                <?php } ?>
            </div>
            
            <div class="card-icon">
                <i class="fas fa-server"></i>
            </div>
            
            <div class="card-content">
                <h3 class="card-title"><?php print $download['name']; ?></h3>
                
                <div class="card-details">
                    <div class="detail-item">
                        <i class="fas fa-hdd"></i>
                        <span>Dimensione: <strong>~2.5 GB</strong></span>
                    </div>
                    <div class="detail-item">
                        <i class="fas fa-code-branch"></i>
                        <span>Versione: <strong>1.0.0</strong></span>
                    </div>
                    <div class="detail-item">
                        <i class="fas fa-shield-alt"></i>
                        <span>Sicuro e verificato</span>
                    </div>
                </div>
            </div>
            
            <a href="<?php print $download['link']; ?>" class="download-btn" target="_blank">
                <i class="fas fa-download"></i>
                <span>Scarica Ora</span>
                <div class="btn-glow"></div>
            </a>
            
            <div class="card-footer">
                <span><i class="fas fa-info-circle"></i> Compatibile con Windows 7, 8, 10, 11</span>
            </div>
        </div>
        <?php $i++; } ?>
    </div>
    
    <div class="download-instructions">
        <h2 class="instructions-title">
            <i class="fas fa-question-circle"></i>
            Come installare il client
        </h2>
        
        <div class="instructions-grid">
            <div class="instruction-step">
                <div class="step-number">1</div>
                <div class="step-icon"><i class="fas fa-download"></i></div>
                <h4>Scarica il Client</h4>
                <p>Clicca sul pulsante "Scarica Ora" per avviare il download del client ufficiale</p>
            </div>
            
            <div class="instruction-step">
                <div class="step-number">2</div>
                <div class="step-icon"><i class="fas fa-file-archive"></i></div>
                <h4>Estrai i File</h4>
                <p>Una volta completato il download, estrai l'archivio in una cartella a tua scelta</p>
            </div>
            
            <div class="instruction-step">
                <div class="step-number">3</div>
                <div class="step-icon"><i class="fas fa-cog"></i></div>
                <h4>Avvia il Launcher</h4>
                <p>Apri il launcher del gioco e attendi il completamento dell'installazione</p>
            </div>
            
            <div class="instruction-step">
                <div class="step-number">4</div>
                <div class="step-icon"><i class="fas fa-gamepad"></i></div>
                <h4>Gioca!</h4>
                <p>Inserisci le tue credenziali e inizia la tua avventura nel mondo di ONE</p>
            </div>
        </div>
    </div>
    
    <div class="download-faq">
        <h2 class="faq-title">
            <i class="fas fa-comments"></i>
            Domande Frequenti
        </h2>
        
        <div class="faq-list">
            <div class="faq-item">
                <div class="faq-question">
                    <i class="fas fa-chevron-right"></i>
                    <span>Il download è sicuro?</span>
                </div>
                <div class="faq-answer">
                    Sì, tutti i nostri file sono verificati e privi di virus. Utilizziamo server sicuri e criptati.
                </div>
            </div>
            
            <div class="faq-item">
                <div class="faq-question">
                    <i class="fas fa-chevron-right"></i>
                    <span>Quanto spazio occupa il gioco?</span>
                </div>
                <div class="faq-answer">
                    Il client richiede circa 2.5 GB di spazio su disco. Assicurati di avere spazio sufficiente.
                </div>
            </div>
            
            <div class="faq-item">
                <div class="faq-question">
                    <i class="fas fa-chevron-right"></i>
                    <span>Problemi con il download?</span>
                </div>
                <div class="faq-answer">
                    Se hai problemi, prova con un mirror alternativo o contatta il supporto su Discord.
                </div>
            </div>
        </div>
    </div>
    
    <?php } else { ?>
    <div class="no-downloads">
        <div class="no-downloads-icon">
            <i class="fas fa-exclamation-triangle"></i>
        </div>
        <h3>Nessun Download Disponibile</h3>
        <p>Al momento non ci sono link di download disponibili. Riprova più tardi.</p>
    </div>
    <?php } ?>
</div>

<style>
/* =================================
   DOWNLOAD PAGE - DESIGN EPICO
   ================================= */
.download-page {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
}

/* Hero Section */
.download-hero {
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.2) 0%, rgba(192, 57, 43, 0.1) 100%);
    border: 1px solid rgba(231, 76, 60, 0.3);
    border-radius: 16px;
    padding: 60px 40px;
    margin-bottom: 50px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.download-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(231, 76, 60, 0.1) 0%, transparent 70%);
    animation: heroGlow 8s ease-in-out infinite;
}

@keyframes heroGlow {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.5; }
    50% { transform: translate(10%, 10%) scale(1.1); opacity: 1; }
}

.download-hero-content {
    position: relative;
    z-index: 1;
}

.hero-icon {
    width: 100px;
    height: 100px;
    margin: 0 auto 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
    border-radius: 50%;
    box-shadow: 0 10px 40px rgba(231, 76, 60, 0.5);
    animation: iconFloat 3s ease-in-out infinite;
}

@keyframes iconFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.hero-icon i {
    font-size: 50px;
    color: white;
}

.download-title {
    font-family: var(--font-secondary);
    font-size: 48px;
    font-weight: 900;
    color: var(--color-text-light);
    margin: 0 0 15px 0;
    text-transform: uppercase;
    letter-spacing: 3px;
    text-shadow: 0 4px 20px rgba(231, 76, 60, 0.5);
}

.download-subtitle {
    font-size: 18px;
    color: var(--color-text-dark);
    margin: 0;
}

/* Download Grid */
.download-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
    gap: 30px;
    margin-bottom: 60px;
}

.download-card {
    background: var(--color-box-bg);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 35px;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    animation: cardFadeIn 0.6s ease-out;
}

@keyframes cardFadeIn {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.download-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.05) 0%, transparent 100%);
    opacity: 0;
    transition: opacity 0.4s ease;
}

.download-card:hover {
    transform: translateY(-10px);
    border-color: rgba(231, 76, 60, 0.5);
    box-shadow: 0 20px 60px rgba(231, 76, 60, 0.3);
}

.download-card:hover::before {
    opacity: 1;
}

.card-badge {
    position: absolute;
    top: 20px;
    right: 20px;
}

.card-badge span {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge-primary {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
    color: #1a0a0a;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
}

.badge-mirror {
    background: rgba(255, 255, 255, 0.1);
    color: var(--color-text-light);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.card-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(231, 76, 60, 0.15);
    border: 2px solid rgba(231, 76, 60, 0.3);
    border-radius: 16px;
    transition: all 0.4s ease;
}

.download-card:hover .card-icon {
    background: rgba(231, 76, 60, 0.25);
    border-color: rgba(231, 76, 60, 0.5);
    transform: scale(1.1) rotate(5deg);
}

.card-icon i {
    font-size: 40px;
    color: var(--color-primary);
}

.card-content {
    text-align: center;
    margin-bottom: 30px;
}

.card-title {
    font-family: var(--font-secondary);
    font-size: 24px;
    font-weight: 700;
    color: var(--color-text-light);
    margin: 0 0 20px 0;
    text-transform: uppercase;
}

.card-details {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.detail-item {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    color: var(--color-text-dark);
    font-size: 14px;
}

.detail-item i {
    color: var(--color-primary);
    font-size: 16px;
}

.detail-item strong {
    color: var(--color-text-light);
}

/* Download Button */
.download-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    width: 100%;
    padding: 18px 30px;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
    border: none;
    border-radius: 10px;
    color: white;
    font-size: 18px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.4s ease;
    box-shadow: 0 8px 25px rgba(231, 76, 60, 0.4);
}

.download-btn::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    transform: translate(-50%, -50%);
    transition: width 0.6s ease, height 0.6s ease;
}

.download-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(231, 76, 60, 0.6);
}

.download-btn:hover::before {
    width: 300px;
    height: 300px;
}

.download-btn i {
    font-size: 22px;
    position: relative;
    z-index: 1;
}

.download-btn span {
    position: relative;
    z-index: 1;
}

.btn-glow {
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    transition: left 0.5s ease;
}

.download-btn:hover .btn-glow {
    left: 100%;
}

.card-footer {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    text-align: center;
}

.card-footer span {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--color-text-dark);
}

.card-footer i {
    color: var(--color-primary);
}

/* Instructions Section */
.download-instructions {
    background: var(--color-box-bg);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 50px 40px;
    margin-bottom: 50px;
}

.instructions-title {
    font-family: var(--font-secondary);
    font-size: 32px;
    font-weight: 700;
    color: var(--color-primary);
    text-align: center;
    margin: 0 0 40px 0;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.instructions-title i {
    font-size: 36px;
}

.instructions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
}

.instruction-step {
    text-align: center;
    padding: 30px 20px;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    position: relative;
    transition: all 0.3s ease;
}

.instruction-step:hover {
    transform: translateY(-5px);
    border-color: rgba(231, 76, 60, 0.3);
    box-shadow: 0 10px 30px rgba(231, 76, 60, 0.2);
}

.step-number {
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
    border-radius: 50%;
    font-size: 20px;
    font-weight: 700;
    color: white;
    box-shadow: 0 4px 15px rgba(231, 76, 60, 0.5);
}

.step-icon {
    width: 70px;
    height: 70px;
    margin: 20px auto 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(231, 76, 60, 0.1);
    border: 2px solid rgba(231, 76, 60, 0.3);
    border-radius: 50%;
    transition: all 0.3s ease;
}

.instruction-step:hover .step-icon {
    background: rgba(231, 76, 60, 0.2);
    transform: scale(1.1);
}

.step-icon i {
    font-size: 32px;
    color: var(--color-primary);
}

.instruction-step h4 {
    font-size: 18px;
    font-weight: 700;
    color: var(--color-text-light);
    margin: 0 0 12px 0;
}

.instruction-step p {
    font-size: 14px;
    color: var(--color-text-dark);
    line-height: 1.6;
    margin: 0;
}

/* FAQ Section */
.download-faq {
    background: var(--color-box-bg);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 50px 40px;
}

.faq-title {
    font-family: var(--font-secondary);
    font-size: 32px;
    font-weight: 700;
    color: var(--color-primary);
    text-align: center;
    margin: 0 0 40px 0;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.faq-title i {
    font-size: 36px;
}

.faq-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-width: 900px;
    margin: 0 auto;
}

.faq-item {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.faq-item:hover {
    border-color: rgba(231, 76, 60, 0.3);
}

.faq-question {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 20px 25px;
    font-size: 16px;
    font-weight: 600;
    color: var(--color-text-light);
    cursor: pointer;
    transition: all 0.3s ease;
}

.faq-question:hover {
    color: var(--color-primary);
}

.faq-question i {
    color: var(--color-primary);
    font-size: 14px;
    transition: transform 0.3s ease;
}

.faq-item:hover .faq-question i {
    transform: translateX(5px);
}

.faq-answer {
    padding: 0 25px 20px 55px;
    font-size: 14px;
    color: var(--color-text-dark);
    line-height: 1.8;
}

/* No Downloads State */
.no-downloads {
    text-align: center;
    padding: 80px 40px;
    background: var(--color-box-bg);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
}

.no-downloads-icon {
    width: 100px;
    height: 100px;
    margin: 0 auto 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(231, 76, 60, 0.1);
    border: 2px solid rgba(231, 76, 60, 0.3);
    border-radius: 50%;
}

.no-downloads-icon i {
    font-size: 50px;
    color: var(--color-primary);
}

.no-downloads h3 {
    font-size: 28px;
    color: var(--color-text-light);
    margin: 0 0 15px 0;
}

.no-downloads p {
    font-size: 16px;
    color: var(--color-text-dark);
    margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
    .download-hero {
        padding: 40px 25px;
    }
    
    .download-title {
        font-size: 32px;
    }
    
    .download-grid {
        grid-template-columns: 1fr;
    }
    
    .instructions-grid {
        grid-template-columns: 1fr;
    }
    
    .download-instructions,
    .download-faq {
        padding: 30px 20px;
    }
}
</style>