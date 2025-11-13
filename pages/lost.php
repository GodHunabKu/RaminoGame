<div class="account-page-modern">
    <div class="account-hero">
        <div class="account-hero-content">
            <div class="hero-icon">
                <i class="fas fa-life-ring"></i>
            </div>
            <h1 class="account-title"><?php if($message==7) print 'Cambia Password'; else print 'Recupero Password'; ?></h1>
            <p class="account-subtitle">Recupera l'accesso al tuo account</p>
        </div>
    </div>

    <div class="login-container">
        <div class="login-form-wrapper">
            <form role="form" method="post" action="" class="modern-login-form">
                <?php
                    if(isset($_GET['email']) && isset($_GET['code']) && !empty($_GET['email']) && !empty($_GET['code']) && isValidEmail($_GET['email']))
                    {
                        $alert_type = 'danger';
                        $alert_icon = 'fa-exclamation-circle';
                        $alert_message = '';

                        if($message==6)
                        {
                            $alert_message = htmlspecialchars($lang['incorrect-recovery'], ENT_QUOTES, 'UTF-8');
                        }
                        else if(isset($_POST['password']) && isset($_POST['rpassword']) && $message==9)
                        {
                            $message = 7;
                            $alert_message = htmlspecialchars($lang['no-password-r'], ENT_QUOTES, 'UTF-8');
                        }
                        else if(isset($_POST['password']) && isset($_POST['rpassword']) && $message==8)
                        {
                            $message = 11;
                            $alert_type = 'success';
                            $alert_icon = 'fa-check-circle';
                            $alert_message = htmlspecialchars($lang['success-change-password'], ENT_QUOTES, 'UTF-8');
                        }
                        else if(isset($_POST['password']) && isset($_POST['rpassword']) && $message==10)
                        {
                            $message = 7;
                            $alert_message = htmlspecialchars($lang['incorrect-password'], ENT_QUOTES, 'UTF-8');
                        }

                        if($alert_message) {
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
                        }
                    } else if(isset($_POST['username']) && isset($_POST['email']) && isset($_POST['captcha']))
                    {
                        $alert_type = 'danger';
                        $alert_icon = 'fa-exclamation-circle';
                        $alert_message = '';

                        if($message==5)
                        {
                            $alert_message = htmlspecialchars($lang['incorrect-security'], ENT_QUOTES, 'UTF-8');

                            print '<div class="alert-modern alert-'.$alert_type.'">
                                      <div class="alert-icon"><i class="fas '.$alert_icon.'"></i></div>
                                      <div class="alert-content">
                                          <strong>Attenzione!</strong>
                                          <p>'.$alert_message.'</p>
                                      </div>
                                      <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                                          <i class="fas fa-times"></i>
                                      </button>
                                  </div>';
                        }
                        else {
                            print '<div class="alert-modern alert-info">
                                      <div class="alert-icon"><i class="fas fa-info-circle"></i></div>
                                      <div class="alert-content">
                                          <strong>Email Inviata!</strong>
                                          <p>'.htmlspecialchars($lang['email-recovery'], ENT_QUOTES, 'UTF-8').'</p>
                                      </div>
                                      <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                                          <i class="fas fa-times"></i>
                                      </button>
                                  </div>';

                            if($message==1)
                            {
                                $alt_message = $lang['code-delete-chars'];
                                $subject = $lang['account-recovery'];
                                $sendName = $_POST['username'];
                                $sendEmail = $_POST['email'];

                                $code = generateSocialID(32);
                                update_passlost_token($_POST['username'], $code);
                                $html_mail = recoveryPassword($code, $_POST['email'], $_POST['username']);
                                include 'include/functions/sendEmail.php';
                            }
                        }
                    }
                    require 'include/captcha/simple.php';
                    $_SESSION['captcha_lost'] = simple_php_captcha();

                if($message!=11) {
                ?>

                <div class="form-section">
                    <h3 class="section-title">
                        <i class="fas fa-<?php if($message==7) print 'key'; else print 'user-shield'; ?>"></i>
                        <?php if($message==7) print 'Nuova Password'; else print 'Dati Account'; ?>
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
                        <label for="username">
                            <i class="fas fa-user"></i>
                            <?php print htmlspecialchars($lang['user-name'], ENT_QUOTES, 'UTF-8'); ?>
                        </label>
                        <input
                            class="form-control-modern"
                            name="username"
                            id="username"
                            pattern=".{5,16}"
                            maxlength="16"
                            placeholder="<?php print htmlspecialchars($lang['user-name'], ENT_QUOTES, 'UTF-8'); ?>..."
                            required
                            type="text"
                            autocomplete="off"
                        >
                        <div class="input-border"></div>
                    </div>

                    <div class="form-group-modern">
                        <label for="email">
                            <i class="fas fa-envelope"></i>
                            <?php print htmlspecialchars($lang['email-address'], ENT_QUOTES, 'UTF-8'); ?>
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
                        <label for="captcha">
                            <i class="fas fa-shield-alt"></i>
                            Verifica di Sicurezza
                        </label>
                        <div class="captcha-wrapper">
                            <?php print '<img src="'.$site_url.'include/captcha/simple.php'.$_SESSION['captcha_lost']['image_src'].'" alt="Captcha">'; ?>
                        </div>
                        <input
                            class="form-control-modern"
                            name="captcha"
                            id="captcha"
                            pattern=".{4,6}"
                            maxlength="5"
                            placeholder="<?php print htmlspecialchars($lang['captcha-code'], ENT_QUOTES, 'UTF-8'); ?>"
                            required
                            type="text"
                            style="margin-top: 15px; text-align: center; font-size: 24px; letter-spacing: 5px;"
                        >
                        <div class="input-border"></div>
                    </div>
                    <?php } ?>
                </div>

                <button type="submit" class="btn-submit-modern">
                    <span class="btn-text">
                        <i class="fas fa-<?php if($message==7) print 'save'; else print 'paper-plane'; ?>"></i>
                        <?php if($message==7) print htmlspecialchars($lang['change-password'], ENT_QUOTES, 'UTF-8'); else print htmlspecialchars($lang['account-recovery'], ENT_QUOTES, 'UTF-8'); ?>
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
