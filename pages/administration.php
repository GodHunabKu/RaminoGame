<!-- PAGINA ACCOUNT - VERSIONE 2.0 OTTIMIZZATA -->
<div class="admin-page-v2">
    <?php
        $account_name = getAccountName($_SESSION['id']);

        // Gestione azioni POST con sistema email ottimizzato
        $notification = null;

        if(isset($_POST['delete-code'])) {
            $code = getAccountSocialID($_SESSION['id']);
            $html_mail = sendCode($account_name, $code, 1);
            $alt_message = $lang['delete-chars'];
            $subject = $lang['delete-chars'];
            $sendName = $account_name;
            $sendEmail = $myEmail;
            include 'include/functions/sendEmail.php';

            $notification = $email_sent_successfully ?
                ['type' => 'success', 'title' => 'Email Inviata!', 'message' => $lang['sended-code']] :
                ['type' => 'error', 'title' => 'Errore', 'message' => 'Impossibile inviare l\'email'];
        }

        if(isset($_POST['storekeeper-code'])) {
            $code = getPlayerSafeBoxPassword($_SESSION['id']);

            if($code != '' && $code != '000000') {
                $html_mail = sendCode($account_name, $code, 2);
                $alt_message = $lang['storekeeper'];
                $subject = $lang['storekeeper'];
                $sendName = $account_name;
                $sendEmail = $myEmail;
                include 'include/functions/sendEmail.php';

                $notification = $email_sent_successfully ?
                    ['type' => 'success', 'title' => 'Email Inviata!', 'message' => $lang['sended-code']] :
                    ['type' => 'error', 'title' => 'Errore', 'message' => 'Impossibile inviare l\'email'];
            } else {
                $notification = ['type' => 'warning', 'title' => 'Attenzione!', 'message' => $lang['no-storekeeper']];
            }
        }

        if(isset($_POST['change-password'])) {
            $code = generateSocialID(32);
            update_passlost_token_by_email($myEmail, $code);
            $code_link = '<br><br><a href="'.$site_url.'user/password/'.$code.'" target="_blank" style="display: inline-block; color: #ffffff; background-color: #3498db; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; cursor: pointer; text-decoration: none; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-transform: capitalize; border-color: #3498db;">'.$lang['change-password'].'</a>';

            $html_mail = sendCode($account_name, $code_link, 4);
            $alt_message = $lang['password'];
            $subject = $lang['password'];
            $sendName = $account_name;
            $sendEmail = $myEmail;
            include 'include/functions/sendEmail.php';

            $notification = $email_sent_successfully ?
                ['type' => 'success', 'title' => 'Email Inviata!', 'message' => $lang['sended-code']] :
                ['type' => 'error', 'title' => 'Errore', 'message' => 'Impossibile inviare l\'email'];
        }
    ?>

    <!-- Header -->
    <div class="admin-header">
        <div class="admin-header-content">
            <div class="header-icon">
                <i class="fas fa-user-circle"></i>
            </div>
            <div class="header-text">
                <h1><?php print $lang['my-account']; ?></h1>
                <p>Benvenuto, <strong><?php echo htmlspecialchars($account_name, ENT_QUOTES, 'UTF-8'); ?></strong></p>
            </div>
        </div>
    </div>

    <!-- Notification System -->
    <?php if($notification): ?>
    <div class="notification notification-<?php echo $notification['type']; ?>" id="mainNotification">
        <div class="notification-icon">
            <i class="fas fa-<?php
                echo $notification['type'] == 'success' ? 'check-circle' :
                    ($notification['type'] == 'warning' ? 'exclamation-triangle' : 'times-circle');
            ?>"></i>
        </div>
        <div class="notification-content">
            <strong><?php echo $notification['title']; ?></strong>
            <p><?php echo $notification['message']; ?></p>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    </div>
    <?php endif; ?>

    <!-- Stats Cards -->
    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-icon stat-icon-blue">
                <i class="fas fa-user"></i>
            </div>
            <div class="stat-content">
                <span class="stat-label"><?php print $lang['user-name']; ?></span>
                <span class="stat-number"><?php echo htmlspecialchars($account_name, ENT_QUOTES, 'UTF-8'); ?></span>
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-icon stat-icon-green">
                <i class="fas fa-envelope"></i>
            </div>
            <div class="stat-content">
                <span class="stat-label"><?php print $lang['email-address']; ?></span>
                <span class="stat-number"><?php echo htmlspecialchars($myEmail, ENT_QUOTES, 'UTF-8'); ?></span>
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-icon stat-icon-gold">
                <i class="fas fa-coins"></i>
            </div>
            <div class="stat-content">
                <span class="stat-label"><?php print $lang['md']; ?></span>
                <span class="stat-number"><?php print number_format(getAccountMD($_SESSION['id'])); ?></span>
            </div>
        </div>
    </div>

    <!-- Actions Section -->
    <div class="actions-container">
        <h2 class="actions-title">
            <i class="fas fa-cogs"></i>
            Gestione Account
        </h2>

        <div class="actions-grid">
            <!-- View Characters -->
            <div class="action-item">
                <div class="action-icon-wrap">
                    <i class="fas fa-users"></i>
                </div>
                <h3><?php print $lang['chars']; ?></h3>
                <p><?php print $lang['chars-list']; ?></p>
                <a href="<?php print $site_url; ?>user/characters" class="action-btn action-btn-primary">
                    Visualizza
                    <i class="fas fa-arrow-right"></i>
                </a>
            </div>

            <!-- Change Email -->
            <div class="action-item">
                <div class="action-icon-wrap">
                    <i class="fas fa-at"></i>
                </div>
                <h3><?php print $lang['email-address']; ?></h3>
                <p><?php print $lang['change-email']; ?></p>
                <a href="<?php print $site_url; ?>user/email" class="action-btn action-btn-primary">
                    Modifica
                    <i class="fas fa-arrow-right"></i>
                </a>
            </div>

            <!-- Change Password -->
            <div class="action-item">
                <div class="action-icon-wrap">
                    <i class="fas fa-key"></i>
                </div>
                <h3><?php print $lang['password']; ?></h3>
                <p><?php print $lang['change-password']; ?></p>
                <form action="" method="post" style="width: 100%;">
                    <button type="submit" name="change-password" class="action-btn action-btn-primary"
                            onclick="return confirm('<?php print $lang['sure_send?']; ?>')">
                        Cambia
                        <i class="fas fa-arrow-right"></i>
                    </button>
                </form>
            </div>

            <!-- Storekeeper Password -->
            <div class="action-item">
                <div class="action-icon-wrap">
                    <i class="fas fa-warehouse"></i>
                </div>
                <h3><?php print $lang['storekeeper']; ?></h3>
                <p><?php print $lang['request-storekeeper']; ?></p>
                <form action="" method="post" style="width: 100%;">
                    <button type="submit" name="storekeeper-code" class="action-btn action-btn-primary"
                            onclick="return confirm('<?php print $lang['sure_send?']; ?>')">
                        Richiedi
                        <i class="fas fa-arrow-right"></i>
                    </button>
                </form>
            </div>

            <!-- Delete Characters Code -->
            <div class="action-item action-item-warning">
                <div class="action-icon-wrap">
                    <i class="fas fa-user-minus"></i>
                </div>
                <h3><?php print $lang['delete-chars']; ?></h3>
                <p>Invia il codice per cancellare i personaggi</p>
                <form action="" method="post" style="width: 100%;">
                    <button type="submit" name="delete-code" class="action-btn action-btn-warning"
                            onclick="return confirm('<?php print $lang['sure_send?']; ?>')">
                        Invia Codice
                        <i class="fas fa-arrow-right"></i>
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>

<!-- Link CSS dedicato -->
<link rel="stylesheet" href="<?php print $site_url; ?>css/administration-v2.css?v=<?php echo time(); ?>">

<!-- Link JS dedicato -->
<script src="<?php print $site_url; ?>js/administration-v2.js?v=<?php echo time(); ?>"></script>
