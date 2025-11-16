<div class="register-page">
    <div class="register-hero">
        <div class="register-hero-content">
            <div class="hero-icon">
                <i class="fas fa-user-plus"></i>
            </div>
            <h1 class="register-title">CREA IL TUO ACCOUNT</h1>
            <p class="register-subtitle">Unisciti alla community di ONE e inizia la tua leggenda!</p>
        </div>
    </div>

    <?php if($jsondataFunctions['active-registrations']==1) { ?>
    <div class="register-container">
        <div class="register-form-wrapper">
            <form role="form" method="post" action="" class="modern-register-form">
                <?php include 'include/functions/register.php'; ?>

                <div class="form-section">
                    <h3 class="section-title">
                        <i class="fas fa-user-circle"></i>
                        Informazioni Account
                    </h3>
                    
                    <div class="form-group-modern">
                        <label for="username">
                            <i class="fas fa-user"></i>
                            Username
                        </label>
                        <input 
                            class="form-control-modern" 
                            name="username" 
                            id="username" 
                            pattern=".{5,16}" 
                            maxlength="16" 
                            placeholder="Inserisci il tuo username (5-16 caratteri)" 
                            required 
                            type="text" 
                            autocomplete="off"
                        >
                        <div class="field-requirements">
                            <span><i class="fas fa-info-circle"></i> Solo lettere e numeri</span>
                        </div>
                        <p class="text-danger" id="checkname"></p>
                        <p class="text-danger" id="checkname2"></p>
                    </div>
                    
                    <div class="form-group-modern">
                        <label for="email">
                            <i class="fas fa-envelope"></i>
                            Email
                        </label>
                        <input 
                            class="form-control-modern" 
                            name="email" 
                            id="email" 
                            pattern=".{7,64}" 
                            maxlength="64" 
                            placeholder="esempio@email.com" 
                            required 
                            type="email"
                        >
                        <div class="field-requirements">
                            <span><i class="fas fa-info-circle"></i> Indirizzo email valido</span>
                        </div>
                        <p class="text-danger" id="checkemail"></p>
                    </div>
                </div>
                
                <div class="form-section">
                    <h3 class="section-title">
                        <i class="fas fa-lock"></i>
                        Sicurezza
                    </h3>
                    
                    <div class="form-group-modern">
                        <label for="password">
                            <i class="fas fa-key"></i>
                            Password
                        </label>
                        <input 
                            class="form-control-modern" 
                            name="password" 
                            id="password" 
                            pattern=".{5,16}" 
                            maxlength="16" 
                            placeholder="Scegli una password sicura (5-16 caratteri)" 
                            required 
                            type="password"
                        >
                        <div class="password-strength">
                            <div class="strength-bar">
                                <div class="strength-fill" id="strength-fill"></div>
                            </div>
                            <span class="strength-text" id="strength-text">Forza password</span>
                        </div>
                    </div>
                    
                    <div class="form-group-modern">
                        <label for="rpassword">
                            <i class="fas fa-check-double"></i>
                            Conferma Password
                        </label>
                        <input 
                            class="form-control-modern" 
                            name="rpassword" 
                            id="rpassword" 
                            pattern=".{5,16}" 
                            maxlength="16" 
                            placeholder="Ripeti la password" 
                            required 
                            type="password"
                        >
                        <p class="text-danger" id="checkpassword"></p>
                    </div>
                </div>
                
                <div class="form-section">
                    <h3 class="section-title">
                        <i class="fas fa-shield-alt"></i>
                        Verifica di Sicurezza
                    </h3>

                    <div class="recaptcha-wrapper">
                        <div class="g-recaptcha" data-sitekey="<?php print $site_key; ?>" data-theme="dark"></div>
                    </div>
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="btn-register">
                        <i class="fas fa-user-plus"></i>
                        <span>Registrati Ora</span>
                        <div class="btn-glow"></div>
                    </button>
                    
                    <div class="form-footer-text">
                        <p>Hai gi� un account? <a href="<?php echo $site_url; ?>users/login">Accedi qui</a></p>
                    </div>
                </div>
            </form>
        </div>
        
        <div class="register-info">
            <div class="info-card">
                <div class="info-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <h4>Requisiti Account</h4>
                <ul class="requirements-list">
                    <li><i class="fas fa-angle-right"></i> Username: 5-16 caratteri alfanumerici</li>
                    <li><i class="fas fa-angle-right"></i> Password: minimo 5 caratteri</li>
                    <li><i class="fas fa-angle-right"></i> Email valida e funzionante</li>
                    <li><i class="fas fa-angle-right"></i> Completare la verifica captcha</li>
                </ul>
            </div>
            
            <div class="info-card">
                <div class="info-icon">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <h4>Sicurezza & Privacy</h4>
                <ul class="requirements-list">
                    <li><i class="fas fa-angle-right"></i> I tuoi dati sono al sicuro</li>
                    <li><i class="fas fa-angle-right"></i> Password criptate con algoritmi moderni</li>
                    <li><i class="fas fa-angle-right"></i> Nessun dato condiviso con terze parti</li>
                    <li><i class="fas fa-angle-right"></i> Protezione anti-bot e spam</li>
                </ul>
            </div>
            
            <div class="info-card">
                <div class="info-icon">
                    <i class="fas fa-gift"></i>
                </div>
                <h4>Vantaggi Immediati</h4>
                <ul class="requirements-list">
                    <li><i class="fas fa-angle-right"></i> Accesso completo al gioco</li>
                    <li><i class="fas fa-angle-right"></i> Supporto della community</li>
                    <li><i class="fas fa-angle-right"></i> Aggiornamenti esclusivi</li>
                    <li><i class="fas fa-angle-right"></i> Eventi e premi speciali</li>
                </ul>
            </div>
        </div>
    </div>
    
    <?php } else { ?>
    <div class="registrations-disabled">
        <div class="disabled-icon">
            <i class="fas fa-user-lock"></i>
        </div>
        <h3>Registrazioni Temporaneamente Chiuse</h3>
        <p><?php print $lang['disabled-registrations']; ?></p>
        <a href="<?php echo $site_url; ?>" class="btn-back">
            <i class="fas fa-arrow-left"></i>
            Torna alla Homepage
        </a>
    </div>
    <?php } ?>
</div>

<style>
/* =================================
   REGISTER PAGE - DESIGN MODERNO
   ================================= */
.register-page {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
}

/* Hero Section */
.register-hero {
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.2) 0%, rgba(192, 57, 43, 0.1) 100%);
    border: 1px solid rgba(231, 76, 60, 0.3);
    border-radius: 16px;
    padding: 50px 40px;
    margin-bottom: 50px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.register-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(231, 76, 60, 0.1) 0%, transparent 70%);
    animation: heroGlow 8s ease-in-out infinite;
}

.register-hero-content {
    position: relative;
    z-index: 1;
}

.hero-icon {
    width: 90px;
    height: 90px;
    margin: 0 auto 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
    border-radius: 50%;
    box-shadow: 0 10px 40px rgba(231, 76, 60, 0.5);
    animation: iconFloat 3s ease-in-out infinite;
}

.hero-icon i {
    font-size: 45px;
    color: white;
}

.register-title {
    font-family: var(--font-secondary);
    font-size: 42px;
    font-weight: 900;
    color: var(--color-text-light);
    margin: 0 0 12px 0;
    text-transform: uppercase;
    letter-spacing: 2px;
    text-shadow: 0 4px 20px rgba(231, 76, 60, 0.5);
}

.register-subtitle {
    font-size: 17px;
    color: var(--color-text-dark);
    margin: 0;
}

/* Register Container */
.register-container {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 40px;
    align-items: start;
}

/* Form Wrapper */
.register-form-wrapper {
    background: var(--color-box-bg);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 40px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.modern-register-form {
    display: flex;
    flex-direction: column;
    gap: 35px;
}

/* Form Section */
.form-section {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: var(--font-secondary);
    font-size: 20px;
    font-weight: 700;
    color: var(--color-primary);
    text-transform: uppercase;
    margin: 0 0 10px 0;
    padding-bottom: 12px;
    border-bottom: 2px solid rgba(231, 76, 60, 0.3);
}

.section-title i {
    font-size: 22px;
}

/* Form Group */
.form-group-modern {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group-modern label {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    font-weight: 600;
    color: var(--color-text-light);
    margin: 0;
}

.form-group-modern label i {
    color: var(--color-primary);
    font-size: 16px;
}

.form-control-modern {
    width: 100%;
    padding: 15px 18px;
    background: rgba(0, 0, 0, 0.4);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: var(--color-text-light);
    font-size: 15px;
    transition: all 0.3s ease;
}

.form-control-modern::placeholder {
    color: rgba(255, 255, 255, 0.3);
}

.form-control-modern:focus {
    outline: none;
    border-color: var(--color-primary);
    background: rgba(0, 0, 0, 0.5);
    box-shadow: 0 0 20px rgba(231, 76, 60, 0.3);
}

.field-requirements {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: var(--color-text-dark);
}

.field-requirements i {
    color: var(--color-primary);
}

/* Password Strength */
.password-strength {
    margin-top: 8px;
}

.strength-bar {
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 6px;
}

.strength-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #E74C3C 0%, #27AE60 100%);
    border-radius: 3px;
    transition: width 0.3s ease, background 0.3s ease;
}

.strength-text {
    font-size: 12px;
    color: var(--color-text-dark);
}

/* reCAPTCHA Container */
.recaptcha-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 25px;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
}

.recaptcha-wrapper .g-recaptcha {
    transform: scale(0.95);
    transform-origin: center;
}

/* Form Actions */
.form-actions {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 15px;
}

.btn-register {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    width: 100%;
    padding: 18px 30px;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
    border: none;
    border-radius: 12px;
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

.btn-register::before {
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

.btn-register:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(231, 76, 60, 0.6);
}

.btn-register:hover::before {
    width: 400px;
    height: 400px;
}

.btn-register i {
    font-size: 20px;
    position: relative;
    z-index: 1;
}

.btn-register span {
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

.btn-register:hover .btn-glow {
    left: 100%;
}

.form-footer-text {
    text-align: center;
}

.form-footer-text p {
    font-size: 14px;
    color: var(--color-text-dark);
    margin: 0;
}

.form-footer-text a {
    color: var(--color-primary);
    font-weight: 600;
    transition: color 0.3s ease;
}

.form-footer-text a:hover {
    color: var(--color-primary-dark);
}

/* Register Info Sidebar */
.register-info {
    display: flex;
    flex-direction: column;
    gap: 25px;
    position: sticky;
    top: 130px;
}

.info-card {
    background: var(--color-box-bg);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 25px;
    transition: all 0.3s ease;
}

.info-card:hover {
    border-color: rgba(231, 76, 60, 0.3);
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(231, 76, 60, 0.2);
}

.info-icon {
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(231, 76, 60, 0.15);
    border: 2px solid rgba(231, 76, 60, 0.3);
    border-radius: 12px;
    margin-bottom: 15px;
}

.info-icon i {
    font-size: 28px;
    color: var(--color-primary);
}

.info-card h4 {
    font-size: 18px;
    font-weight: 700;
    color: var(--color-text-light);
    margin: 0 0 15px 0;
}

.requirements-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    list-style: none;
    padding: 0;
    margin: 0;
}

.requirements-list li {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    color: var(--color-text-dark);
    line-height: 1.5;
}

.requirements-list li i {
    color: var(--color-primary);
    font-size: 12px;
}

/* Registrations Disabled */
.registrations-disabled {
    text-align: center;
    padding: 80px 40px;
    background: var(--color-box-bg);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
}

.disabled-icon {
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

.disabled-icon i {
    font-size: 50px;
    color: var(--color-primary);
}

.registrations-disabled h3 {
    font-size: 28px;
    color: var(--color-text-light);
    margin: 0 0 15px 0;
}

.registrations-disabled p {
    font-size: 16px;
    color: var(--color-text-dark);
    margin: 0 0 30px 0;
}

.btn-back {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 15px 30px;
    background: var(--color-primary);
    color: white;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
}

.btn-back:hover {
    background: var(--color-primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(231, 76, 60, 0.5);
}

/* Error Messages - mostra icona SOLO quando c'è un errore */
.text-danger {
    font-size: 13px;
    color: var(--color-primary) !important;
    font-weight: 600;
    margin: 5px 0 0 0 !important;
    display: flex;
    align-items: center;
    gap: 6px;
}

.text-danger:not(:empty)::before {
    content: '\f071';
    font-family: 'Font Awesome 6 Free';
    font-weight: 900;
}

/* Input validi - bordo verde quando tutto va bene */
.form-control-modern:valid:not(:placeholder-shown) {
    border-color: #28a745 !important;
    box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.1);
}

.form-control-modern:valid:not(:placeholder-shown):focus {
    border-color: #28a745 !important;
    box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.2);
}

/* Input con errori - bordo rosso */
.form-control-modern:invalid:not(:placeholder-shown):not(:focus) {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 2px rgba(231, 76, 60, 0.1);
}

/* Responsive */
@media (max-width: 1200px) {
    .register-container {
        grid-template-columns: 1fr;
    }
    
    .register-info {
        position: static;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        display: grid;
    }
}

@media (max-width: 768px) {
    .register-hero {
        padding: 40px 25px;
    }
    
    .register-title {
        font-size: 28px;
    }
    
    .register-form-wrapper {
        padding: 25px;
    }
    
    .captcha-container {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .register-info {
        grid-template-columns: 1fr;
    }
}
</style>

<script>
// Password Strength Indicator
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const strengthFill = document.getElementById('strength-fill');
    const strengthText = document.getElementById('strength-text');
    
    if (passwordInput && strengthFill && strengthText) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            if (password.length >= 5) strength += 25;
            if (password.length >= 8) strength += 25;
            if (/[A-Z]/.test(password)) strength += 25;
            if (/[0-9]/.test(password)) strength += 25;
            
            strengthFill.style.width = strength + '%';
            
            if (strength === 0) {
                strengthText.textContent = 'Forza password';
                strengthText.style.color = 'var(--color-text-dark)';
            } else if (strength <= 25) {
                strengthText.textContent = 'Debole';
                strengthText.style.color = '#E74C3C';
            } else if (strength <= 50) {
                strengthText.textContent = 'Media';
                strengthText.style.color = '#F39C12';
            } else if (strength <= 75) {
                strengthText.textContent = 'Buona';
                strengthText.style.color = '#3498DB';
            } else {
                strengthText.textContent = 'Forte';
                strengthText.style.color = '#27AE60';
            }
        });
    }
});
</script>