<div class="login-page-modern">
    <div class="login-hero">
        <div class="login-hero-content">
            <div class="hero-icon">
                <i class="fas fa-sign-in-alt"></i>
            </div>
            <h1 class="login-title">BENTORNATO GUERRIERO</h1>
            <p class="login-subtitle">Accedi al tuo account e continua la tua leggenda!</p>
        </div>
    </div>

    <div class="login-container">
        <div class="login-form-wrapper">
            <form role="form" method="post" action="" class="modern-login-form">
                <?php
                    if(isset($_POST['username']) && isset($_POST['password']))
                    {
                        $alert_type = 'danger';
                        $alert_icon = 'fa-exclamation-circle';
                        $alert_message = '';

                        switch ($login_info[0]) {
                            case 1:
                                $alert_type = 'success';
                                $alert_icon = 'fa-check-circle';
                                $alert_message = 'Login effettuato con successo!';
                                break;
                            case 2:
                                $alert_message = $lang['account-blocked'];
                                break;
                            case 3:
                                $alert_message = $lang['error-login'];
                                break;
                            case 4:
                                $alert_message = $lang['error-login-email'];
                                break;
                            case 5:
                                $alert_message = $lang['account-blocked-temporary'].' ('.$login_info[2].')';
                                break;
                            case 6:
                                $alert_message = $lang['incorrect-security'];
                                break;
                            default:
                                $alert_message = 'Errore sconosciuto';
                        }

                        print '<div class="alert-modern alert-'.$alert_type.'">
                                  <div class="alert-icon"><i class="fas '.$alert_icon.'"></i></div>
                                  <div class="alert-content">
                                      <strong>'.($alert_type == 'success' ? 'Successo!' : 'Attenzione!').'</strong>
                                      <p>'.$alert_message.'</p>
                                  </div>
                                  <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                                      <i class="fas fa-times"></i>
                                  </button>
                              </div>';

                        if($login_info[0]==2 || $login_info[0]==5) {
                            print '<div class="alert-modern alert-info">
                                      <div class="alert-icon"><i class="fas fa-info-circle"></i></div>
                                      <div class="alert-content">
                                          <strong>Motivo:</strong>
                                          <p>'.$login_info[1].'</p>
                                      </div>
                                  </div>';
                        }
                    }
                ?>

                <div class="form-section">
                    <h3 class="section-title">
                        <i class="fas fa-user-circle"></i>
                        Credenziali di Accesso
                    </h3>

                    <div class="form-group-modern">
                        <label for="username">
                            <i class="fas fa-user"></i>
                            Username o Email
                        </label>
                        <input
                            class="form-control-modern"
                            name="username"
                            id="username"
                            pattern=".{5,64}"
                            maxlength="64"
                            placeholder="Inserisci il tuo username o email"
                            required
                            type="text"
                            autocomplete="username"
                        >
                        <div class="input-border"></div>
                    </div>

                    <div class="form-group-modern">
                        <label for="password">
                            <i class="fas fa-lock"></i>
                            Password
                        </label>
                        <div class="password-input-wrapper">
                            <input
                                class="form-control-modern"
                                name="password"
                                id="password"
                                pattern=".{5,16}"
                                maxlength="16"
                                placeholder="Inserisci la tua password"
                                required
                                type="password"
                                autocomplete="current-password"
                            >
                            <button type="button" class="toggle-password" onclick="togglePasswordVisibility('password')">
                                <i class="fas fa-eye"></i>
                            </button>
                        </div>
                        <div class="input-border"></div>
                    </div>

                    <div class="form-group-modern">
                        <label for="captcha">
                            <i class="fas fa-shield-alt"></i>
                            Verifica di Sicurezza
                        </label>
                        <div class="captcha-wrapper">
                            <div class="g-recaptcha" data-theme="dark" data-sitekey="<?php print $site_key; ?>"></div>
                        </div>
                    </div>
                </div>

                <button type="submit" class="btn-submit-modern">
                    <span class="btn-text">
                        <i class="fas fa-sign-in-alt"></i>
                        <?php print $lang['login']; ?>
                    </span>
                    <span class="btn-glow"></span>
                </button>
            </form>

            <div class="login-footer">
                <div class="footer-links">
                    <a href="<?php print $site_url; ?>users/register" class="footer-link">
                        <i class="fas fa-user-plus"></i>
                        <span><?php print $lang['register']; ?></span>
                    </a>
                    <div class="divider"></div>
                    <a href="<?php print $site_url; ?>users/lost" class="footer-link">
                        <i class="fas fa-key"></i>
                        <span><?php print $lang['forget-password']; ?></span>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
/* =================================
   LOGIN PAGE - DESIGN MODERNO
   ================================= */
.login-page-modern {
    width: 100%;
    min-height: calc(100vh - 200px);
}

.login-hero {
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.1) 0%, rgba(192, 57, 43, 0.05) 100%);
    border: 1px solid rgba(231, 76, 60, 0.2);
    border-radius: 16px;
    padding: 60px 40px;
    text-align: center;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
}

.login-hero::before {
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
    50% { transform: translate(-10%, -10%) scale(1.1); opacity: 0.8; }
}

.login-hero-content {
    position: relative;
    z-index: 1;
}

.hero-icon {
    width: 100px;
    height: 100px;
    margin: 0 auto 30px;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 30px rgba(231, 76, 60, 0.6);
    animation: heroIconFloat 3s ease-in-out infinite;
}

@keyframes heroIconFloat {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-10px) scale(1.05); }
}

.hero-icon i {
    font-size: 48px;
    color: white;
}

.login-title {
    font-family: var(--font-secondary);
    font-size: 42px;
    color: var(--color-primary);
    margin: 0 0 15px 0;
    text-transform: uppercase;
    letter-spacing: 2px;
    text-shadow: 0 2px 20px rgba(231, 76, 60, 0.4);
}

.login-subtitle {
    font-size: 18px;
    color: var(--color-text-dark);
    margin: 0;
    font-weight: 300;
}

.login-container {
    max-width: 600px;
    margin: 0 auto;
}

.login-form-wrapper {
    background: var(--color-box-bg);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(231, 76, 60, 0.15);
    border-radius: 16px;
    padding: 50px 40px;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}

.login-form-wrapper::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-accent) 100%);
}

/* ALERTS */
.alert-modern {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 30px;
    position: relative;
    animation: alertSlideIn 0.3s ease-out;
}

@keyframes alertSlideIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

.alert-modern.alert-danger {
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.15) 0%, rgba(192, 57, 43, 0.1) 100%);
    border: 1px solid rgba(231, 76, 60, 0.3);
}

.alert-modern.alert-success {
    background: linear-gradient(135deg, rgba(39, 174, 96, 0.15) 0%, rgba(34, 153, 84, 0.1) 100%);
    border: 1px solid rgba(39, 174, 96, 0.3);
}

.alert-modern.alert-info {
    background: linear-gradient(135deg, rgba(52, 152, 219, 0.15) 0%, rgba(41, 128, 185, 0.1) 100%);
    border: 1px solid rgba(52, 152, 219, 0.3);
}

.alert-icon {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
}

.alert-danger .alert-icon i { color: #E74C3C; font-size: 20px; }
.alert-success .alert-icon i { color: #27AE60; font-size: 20px; }
.alert-info .alert-icon i { color: #3498DB; font-size: 20px; }

.alert-content {
    flex: 1;
}

.alert-content strong {
    display: block;
    margin-bottom: 5px;
    font-size: 16px;
    color: var(--color-text-light);
}

.alert-content p {
    margin: 0;
    font-size: 14px;
    color: var(--color-text-dark);
}

.alert-close {
    background: none;
    border: none;
    color: var(--color-text-dark);
    cursor: pointer;
    padding: 5px;
    transition: var(--transition-fast);
}

.alert-close:hover {
    color: var(--color-text-light);
    transform: scale(1.2);
}

/* FORM SECTIONS */
.form-section {
    margin-bottom: 40px;
}

.section-title {
    font-family: var(--font-secondary);
    color: var(--color-primary);
    font-size: 20px;
    margin: 0 0 30px 0;
    display: flex;
    align-items: center;
    gap: 12px;
    text-transform: uppercase;
    padding-bottom: 15px;
    border-bottom: 2px solid rgba(231, 76, 60, 0.2);
}

.section-title i {
    font-size: 24px;
}

.form-group-modern {
    margin-bottom: 25px;
    position: relative;
}

.form-group-modern label {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    font-weight: 600;
    color: var(--color-text-light);
    margin-bottom: 10px;
}

.form-group-modern label i {
    color: var(--color-primary);
    font-size: 16px;
}

.form-control-modern {
    width: 100%;
    padding: 15px 18px;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(231, 76, 60, 0.2);
    border-radius: 8px;
    color: var(--color-text-light);
    font-size: 15px;
    transition: var(--transition-smooth);
}

.form-control-modern:focus {
    outline: none;
    border-color: var(--color-primary);
    background: rgba(0, 0, 0, 0.5);
    box-shadow: 0 0 20px rgba(231, 76, 60, 0.3);
}

.form-control-modern::placeholder {
    color: rgba(255, 255, 255, 0.3);
}

.input-border {
    height: 2px;
    width: 0;
    background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
    transition: width 0.3s ease;
    margin-top: -1px;
    border-radius: 2px;
}

.form-group-modern:focus-within .input-border {
    width: 100%;
}

/* PASSWORD TOGGLE */
.password-input-wrapper {
    position: relative;
}

.toggle-password {
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: var(--color-text-dark);
    cursor: pointer;
    padding: 5px 10px;
    transition: var(--transition-fast);
}

.toggle-password:hover {
    color: var(--color-primary);
}

/* CAPTCHA */
.captcha-wrapper {
    display: flex;
    justify-content: center;
    padding: 15px;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(231, 76, 60, 0.1);
    border-radius: 8px;
}

/* SUBMIT BUTTON */
.btn-submit-modern {
    width: 100%;
    padding: 18px 30px;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 18px;
    font-weight: 700;
    text-transform: uppercase;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-primary);
    transition: var(--transition-smooth);
}

.btn-submit-modern .btn-text {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.btn-submit-modern .btn-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.btn-submit-modern:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-primary-lg);
}

.btn-submit-modern:hover .btn-glow {
    width: 400px;
    height: 400px;
}

.btn-submit-modern:active {
    transform: translateY(-1px);
}

/* FOOTER */
.login-footer {
    margin-top: 40px;
    padding-top: 30px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-links {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
}

.footer-link {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(231, 76, 60, 0.15);
    border-radius: 8px;
    color: var(--color-text-dark);
    font-size: 14px;
    font-weight: 600;
    transition: var(--transition-smooth);
}

.footer-link i {
    font-size: 16px;
    color: var(--color-primary);
}

.footer-link:hover {
    background: rgba(231, 76, 60, 0.1);
    border-color: var(--color-primary);
    color: var(--color-text-light);
    transform: translateY(-2px);
}

.divider {
    width: 1px;
    height: 30px;
    background: rgba(255, 255, 255, 0.1);
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .login-hero {
        padding: 40px 20px;
    }

    .hero-icon {
        width: 80px;
        height: 80px;
    }

    .hero-icon i {
        font-size: 36px;
    }

    .login-title {
        font-size: 32px;
    }

    .login-subtitle {
        font-size: 16px;
    }

    .login-form-wrapper {
        padding: 30px 20px;
    }

    .footer-links {
        flex-direction: column;
        gap: 15px;
    }

    .divider {
        display: none;
    }

    .footer-link {
        width: 100%;
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .login-title {
        font-size: 24px;
    }

    .section-title {
        font-size: 16px;
    }
}
</style>

<script>
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    const button = input.parentElement.querySelector('.toggle-password i');

    if (input.type === 'password') {
        input.type = 'text';
        button.classList.remove('fa-eye');
        button.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        button.classList.remove('fa-eye-slash');
        button.classList.add('fa-eye');
    }
}
</script>
