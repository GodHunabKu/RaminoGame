<div class="account-page-modern">
    <div class="account-hero">
        <div class="account-hero-content">
            <div class="hero-icon">
                <i class="fas fa-envelope"></i>
            </div>
            <h1 class="account-title">Cambia Email</h1>
            <p class="account-subtitle">Aggiorna l'indirizzo email del tuo account</p>
        </div>
    </div>

    <div class="login-container">
        <div class="login-form-wrapper">
            <form role="form" method="post" action="" class="modern-login-form">
                <?php
                    if(isset($_POST['email']) && isset($_POST['captcha']))
                    {
                        $alert_type = 'danger';
                        $alert_icon = 'fa-exclamation-circle';
                        $alert_message = '';

                        if($message==4) {
                            $alert_type = 'info';
                            $alert_icon = 'fa-info-circle';
                            $alert_message = htmlspecialchars($lang['sended-link'], ENT_QUOTES, 'UTF-8');

                            $code = '<br><br><a href="'.$site_url.'user/email/'.$code.'" target="_blank" style="display: inline-block; color: #ffffff; background-color: #3498db; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; cursor: pointer; text-decoration: none; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-transform: capitalize; border-color: #3498db;">'.htmlspecialchars($lang['change-email'], ENT_QUOTES, 'UTF-8').'</a>';

                            $alt_message = $lang['change-email'];
                            $subject = $lang['change-email'];
                            $sendName = getAccountName($_SESSION['id']);
                            $sendEmail = $myEmail;

                            $html_mail = sendCode($_POST['email'], $code, 5);
                            include 'include/functions/sendEmail.php';
                        } else if($message==5) {
                            $alert_message = htmlspecialchars($lang['incorrect-recovery'], ENT_QUOTES, 'UTF-8');
                        } else if($message==3) {
                            $alert_message = htmlspecialchars($lang['incorrect-security'], ENT_QUOTES, 'UTF-8');
                        } else if($message==2) {
                            $alert_message = htmlspecialchars($lang['incorrect-email'], ENT_QUOTES, 'UTF-8');
                        } else if($message==1) {
                            $alert_message = htmlspecialchars($lang['already-email'], ENT_QUOTES, 'UTF-8');
                        }

                        if($alert_message) {
                            print '<div class="alert-modern alert-'.$alert_type.'">
                                      <div class="alert-icon"><i class="fas '.$alert_icon.'"></i></div>
                                      <div class="alert-content">
                                          <strong>'.($alert_type == 'info' ? 'Informazione' : 'Attenzione').'</strong>
                                          <p>'.$alert_message.'</p>
                                      </div>
                                      <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                                          <i class="fas fa-times"></i>
                                      </button>
                                  </div>';
                        }
                    }

                if($message!=11) {
                ?>

                <div class="form-section">
                    <h3 class="section-title">
                        <i class="fas fa-at"></i>
                        <?php if($message==7) print 'Conferma Password'; else print 'Nuova Email'; ?>
                    </h3>

                    <?php if($message==7) { ?>
                    <div class="form-group-modern">
                        <label for="password">
                            <i class="fas fa-lock"></i>
                            <?php print htmlspecialchars($lang['password'], ENT_QUOTES, 'UTF-8'); ?>
                        </label>
                        <div class="password-input-wrapper">
                            <input
                                class="form-control-modern"
                                name="password"
                                id="password"
                                pattern=".{5,16}"
                                maxlength="16"
                                placeholder="<?php print htmlspecialchars($lang['password'], ENT_QUOTES, 'UTF-8'); ?>"
                                required
                                type="password"
                            >
                            <button type="button" class="toggle-password" onclick="togglePasswordVisibility('password')">
                                <i class="fas fa-eye"></i>
                            </button>
                        </div>
                        <div class="input-border"></div>
                    </div>

                    <div class="form-group-modern">
                        <label for="rpassword">
                            <i class="fas fa-lock"></i>
                            <?php print htmlspecialchars($lang['rpassword'], ENT_QUOTES, 'UTF-8'); ?>
                        </label>
                        <div class="password-input-wrapper">
                            <input
                                class="form-control-modern"
                                name="rpassword"
                                id="rpassword"
                                pattern=".{5,16}"
                                maxlength="16"
                                placeholder="<?php print htmlspecialchars($lang['password'], ENT_QUOTES, 'UTF-8'); ?>"
                                required
                                type="password"
                            >
                            <button type="button" class="toggle-password" onclick="togglePasswordVisibility('rpassword')">
                                <i class="fas fa-eye"></i>
                            </button>
                        </div>
                        <div class="input-border"></div>
                        <p class="text-danger" id="checkpassword"></p>
                    </div>
                    <?php } else { ?>
                    <div class="form-group-modern">
                        <label for="email">
                            <i class="fas fa-envelope"></i>
                            <?php print htmlspecialchars($lang['new-email-address'], ENT_QUOTES, 'UTF-8'); ?>
                        </label>
                        <input
                            class="form-control-modern"
                            name="email"
                            id="email"
                            pattern=".{7,64}"
                            maxlength="64"
                            placeholder="<?php print htmlspecialchars($lang['email-address'], ENT_QUOTES, 'UTF-8'); ?>"
                            required
                            type="email"
                        >
                        <div class="input-border"></div>
                    </div>

                    <div class="form-group-modern">
                        <label>
                            <i class="fas fa-shield-alt"></i>
                            Verifica di Sicurezza
                        </label>
                        <div class="recaptcha-wrapper">
                            <div class="g-recaptcha" data-sitekey="<?php print $site_key; ?>" data-theme="dark"></div>
                        </div>
                    </div>
                    <?php } ?>
                </div>

                <button type="submit" class="btn-submit-modern">
                    <span class="btn-text">
                        <i class="fas fa-save"></i>
                        <?php print htmlspecialchars($lang['change-email'], ENT_QUOTES, 'UTF-8'); ?>
                    </span>
                    <span class="btn-glow"></span>
                </button>
            <?php } ?>
            </form>
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
