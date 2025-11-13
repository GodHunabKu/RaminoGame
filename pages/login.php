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
