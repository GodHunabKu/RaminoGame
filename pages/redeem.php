<div class="account-page-modern">
    <div class="account-hero">
        <div class="account-hero-content">
            <div class="hero-icon">
                <i class="fas fa-gift"></i>
            </div>
            <h1 class="account-title"><?php print htmlspecialchars($lang['redeem-codes'], ENT_QUOTES, 'UTF-8'); ?></h1>
            <p class="account-subtitle">Riscatta i tuoi codici promozionali</p>
        </div>
    </div>

    <div class="login-container">
        <div class="login-form-wrapper">
            <?php if($received>=0) {
                $alert_type = (!$received || $received==4) ? 'danger' : 'success';
                $alert_icon = (!$received || $received==4) ? 'fa-exclamation-circle' : 'fa-check-circle';
                $alert_title = (!$received || $received==4) ? 'Errore!' : 'Successo!';
                $alert_message = '';

                if(!$received)
                    $alert_message = htmlspecialchars($lang['incorrect-redeem'], ENT_QUOTES, 'UTF-8');
                else if($received==1 || $received==2)
                {
                    $alert_message = htmlspecialchars($lang['collected_md'], ENT_QUOTES, 'UTF-8').' '.$coins.' ';
                    if($received==1)
                        $alert_message .= htmlspecialchars($lang['md'], ENT_QUOTES, 'UTF-8').' (MD)';
                    else
                        $alert_message .= htmlspecialchars($lang['jd'], ENT_QUOTES, 'UTF-8').' (JD)';
                    $alert_message .= '.';
                }
                else if($received==3)
                    $alert_message = htmlspecialchars($lang['successfully_added'], ENT_QUOTES, 'UTF-8');
                else
                    $alert_message = htmlspecialchars($lang['no_space'], ENT_QUOTES, 'UTF-8');
            ?>
            <div class="alert-modern alert-<?php print $alert_type; ?>">
                <div class="alert-icon"><i class="fas <?php print $alert_icon; ?>"></i></div>
                <div class="alert-content">
                    <strong><?php print $alert_title; ?></strong>
                    <p><?php print $alert_message; ?></p>
                </div>
                <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <?php } ?>

            <form action="" method="POST" class="modern-login-form">
                <div class="form-section">
                    <h3 class="section-title">
                        <i class="fas fa-ticket-alt"></i>
                        Inserisci Codice
                    </h3>

                    <div class="form-group-modern">
                        <label for="code">
                            <i class="fas fa-key"></i>
                            Codice Promozionale
                        </label>
                        <input
                            class="form-control-modern"
                            name="code"
                            id="code"
                            placeholder="Inserisci il tuo codice..."
                            required
                            type="text"
                            style="font-size: 18px; text-align: center; letter-spacing: 2px; text-transform: uppercase;"
                        >
                        <div class="input-border"></div>
                    </div>
                </div>

                <button type="submit" class="btn-submit-modern">
                    <span class="btn-text">
                        <i class="fas fa-check"></i>
                        <?php print htmlspecialchars($lang['redeem-my-code'], ENT_QUOTES, 'UTF-8'); ?>
                    </span>
                    <span class="btn-glow"></span>
                </button>
            </form>
        </div>
    </div>
</div>
