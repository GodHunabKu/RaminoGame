<div class="account-page-modern">
    <div class="account-hero">
        <div class="account-hero-content">
            <div class="hero-icon">
                <i class="fas fa-user-shield"></i>
            </div>
            <h1 class="account-title"><?php print $lang['my-account']; ?></h1>
            <?php $account_name = getAccountName($_SESSION['id']); ?>
            <p class="account-subtitle">Benvenuto, <strong><?php echo htmlspecialchars($account_name, ENT_QUOTES, 'UTF-8'); ?></strong></p>
        </div>
    </div>

    <?php
        // Gestione azioni POST
        if(isset($_POST['delete-code']))
        {
            $alt_message = $lang['delete-chars'];
            $subject = $lang['delete-chars'];
            $sendName = $account_name;
            $sendEmail = $myEmail;
            $code = getAccountSocialID($_SESSION['id']);

            $html_mail = sendCode($account_name, $code);
            include 'include/functions/sendEmail.php';

            print '<div class="alert-modern alert-success">
                      <div class="alert-icon"><i class="fas fa-check-circle"></i></div>
                      <div class="alert-content">
                          <strong>Email Inviata!</strong>
                          <p>'.$lang['sended-code'].'</p>
                      </div>
                      <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                          <i class="fas fa-times"></i>
                      </button>
                  </div>';
        }
        else if(isset($_POST['storekeeper-code']))
        {
            $code = getPlayerSafeBoxPassword($_SESSION['id']);

            if($code!='' && $code!='000000')
            {
                $alt_message = $lang['storekeeper'];
                $subject = $lang['storekeeper'];
                $sendName = $account_name;
                $sendEmail = $myEmail;
                $html_mail = sendCode($account_name, $code, 2);
                include 'include/functions/sendEmail.php';

                print '<div class="alert-modern alert-success">
                          <div class="alert-icon"><i class="fas fa-check-circle"></i></div>
                          <div class="alert-content">
                              <strong>Email Inviata!</strong>
                              <p>'.$lang['sended-code'].'</p>
                          </div>
                          <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                              <i class="fas fa-times"></i>
                          </button>
                      </div>';
            }
            else
            {
                print '<div class="alert-modern alert-danger">
                          <div class="alert-icon"><i class="fas fa-exclamation-circle"></i></div>
                          <div class="alert-content">
                              <strong>Attenzione!</strong>
                              <p>'.$lang['no-storekeeper'].'</p>
                          </div>
                          <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                              <i class="fas fa-times"></i>
                          </button>
                      </div>';
            }
        }
        else if(!$delete_account && isset($_POST['delete-account']))
        {
            $code = generateSocialID(32);
            update_deletion_token($_SESSION['id'], $code);

            $code = '<br><br><a href="'.$site_url.'user/delete/'.$code.'" target="_blank" style="display: inline-block; color: #ffffff; background-color: #3498db; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; cursor: pointer; text-decoration: none; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-transform: capitalize; border-color: #3498db;">'.$lang['delete-account'].'</a>';

            $alt_message = $lang['delete-account'];
            $subject = $lang['delete-account'];
            $sendName = $account_name;
            $sendEmail = $myEmail;
            $html_mail = sendCode($account_name, $code, 3);
            include 'include/functions/sendEmail.php';

            print '<div class="alert-modern alert-success">
                      <div class="alert-icon"><i class="fas fa-check-circle"></i></div>
                      <div class="alert-content">
                          <strong>Email Inviata!</strong>
                          <p>'.$lang['sended-code'].'</p>
                      </div>
                      <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                          <i class="fas fa-times"></i>
                      </button>
                  </div>';
        }
        else if(isset($_POST['change-password']))
        {
            $code = generateSocialID(32);
            update_passlost_token_by_email($myEmail, $code);

            $code = '<br><br><a href="'.$site_url.'user/password/'.$code.'" target="_blank" style="display: inline-block; color: #ffffff; background-color: #3498db; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; cursor: pointer; text-decoration: none; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-transform: capitalize; border-color: #3498db.">'.$lang['change-password'].'</a>';

            $alt_message = $lang['password'];
            $subject = $lang['password'];
            $sendName = $account_name;
            $sendEmail = $myEmail;
            $html_mail = sendCode($account_name, $code, 4);
            include 'include/functions/sendEmail.php';

            print '<div class="alert-modern alert-success">
                      <div class="alert-icon"><i class="fas fa-check-circle"></i></div>
                      <div class="alert-content">
                          <strong>Email Inviata!</strong>
                          <p>'.$lang['sended-code'].'</p>
                      </div>
                      <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                          <i class="fas fa-times"></i>
                      </button>
                  </div>';
        }
    ?>

    <div class="account-container">
        <!-- Account Info Stats -->
        <div class="account-stats">
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-user"></i></div>
                <div class="stat-info">
                    <span class="stat-label"><?php print $lang['user-name']; ?></span>
                    <span class="stat-value"><?php echo htmlspecialchars($account_name, ENT_QUOTES, 'UTF-8'); ?></span>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-envelope"></i></div>
                <div class="stat-info">
                    <span class="stat-label"><?php print $lang['email-address']; ?></span>
                    <span class="stat-value"><?php echo htmlspecialchars($myEmail, ENT_QUOTES, 'UTF-8'); ?></span>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-coins"></i></div>
                <div class="stat-info">
                    <span class="stat-label"><?php print $lang['md']; ?></span>
                    <span class="stat-value"><?php print number_format(getAccountMD($_SESSION['id'])); ?></span>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-gem"></i></div>
                <div class="stat-info">
                    <span class="stat-label"><?php print $lang['jd']; ?></span>
                    <span class="stat-value"><?php print number_format(getAccountJD($_SESSION['id'])); ?></span>
                </div>
            </div>
        </div>

        <!-- Account Actions -->
        <div class="account-actions">
            <h3 class="section-title">
                <i class="fas fa-cogs"></i>
                Gestione Account
            </h3>

            <div class="action-grid">
                <!-- Characters -->
                <div class="action-card">
                    <div class="action-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <div class="action-content">
                        <h4><?php print $lang['chars']; ?></h4>
                        <p><?php print $lang['chars-list']; ?></p>
                    </div>
                    <a href="<?php print $site_url; ?>user/characters" class="action-button">
                        <span>Visualizza</span>
                        <i class="fas fa-arrow-right"></i>
                    </a>
                </div>

                <!-- Change Email -->
                <div class="action-card">
                    <div class="action-icon">
                        <i class="fas fa-at"></i>
                    </div>
                    <div class="action-content">
                        <h4><?php print $lang['email-address']; ?></h4>
                        <p><?php print $lang['change-email']; ?></p>
                    </div>
                    <a href="<?php print $site_url; ?>user/email" class="action-button">
                        <span>Modifica</span>
                        <i class="fas fa-arrow-right"></i>
                    </a>
                </div>

                <!-- Change Password -->
                <div class="action-card">
                    <div class="action-icon">
                        <i class="fas fa-key"></i>
                    </div>
                    <div class="action-content">
                        <h4><?php print $lang['password']; ?></h4>
                        <p><?php print $lang['change-password']; ?></p>
                    </div>
                    <form action="" method="post" class="action-form">
                        <button type="submit" name="change-password" class="action-button" onclick="return confirm('<?php print $lang['sure_send?']; ?>')">
                            <span>Cambia</span>
                            <i class="fas fa-arrow-right"></i>
                        </button>
                    </form>
                </div>

                <!-- Storekeeper -->
                <div class="action-card">
                    <div class="action-icon">
                        <i class="fas fa-warehouse"></i>
                    </div>
                    <div class="action-content">
                        <h4><?php print $lang['storekeeper']; ?></h4>
                        <p><?php print $lang['request-storekeeper']; ?></p>
                    </div>
                    <form action="" method="post" class="action-form">
                        <button type="submit" name="storekeeper-code" class="action-button" onclick="return confirm('<?php print $lang['sure_send?']; ?>')">
                            <span>Richiedi</span>
                            <i class="fas fa-arrow-right"></i>
                        </button>
                    </form>
                </div>

                <!-- Delete Characters -->
                <div class="action-card action-warning">
                    <div class="action-icon">
                        <i class="fas fa-user-minus"></i>
                    </div>
                    <div class="action-content">
                        <h4><?php print $lang['delete-chars']; ?></h4>
                        <p>Invia il codice per cancellare i personaggi</p>
                    </div>
                    <form action="" method="post" class="action-form">
                        <button type="submit" name="delete-code" class="action-button btn-warning" onclick="return confirm('<?php print $lang['sure_send?']; ?>')">
                            <span>Invia Codice</span>
                            <i class="fas fa-arrow-right"></i>
                        </button>
                    </form>
                </div>

                <!-- Delete Account -->
                <?php if(!$delete_account) { ?>
                <div class="action-card action-danger">
                    <div class="action-icon">
                        <i class="fas fa-user-times"></i>
                    </div>
                    <div class="action-content">
                        <h4><?php print $lang['delete-account']; ?></h4>
                        <p>Eliminazione permanente dell'account</p>
                    </div>
                    <form action="" method="post" class="action-form">
                        <button type="submit" name="delete-account" class="action-button btn-danger" onclick="return confirm('<?php print $lang['sure_send?']; ?>')">
                            <span>Elimina</span>
                            <i class="fas fa-arrow-right"></i>
                        </button>
                    </form>
                </div>
                <?php } else { ?>
                <div class="action-card action-info">
                    <div class="action-icon">
                        <i class="fas fa-clock"></i>
                    </div>
                    <div class="action-content">
                        <h4>Account in Eliminazione</h4>
                        <p>
                            <?php
                                $date1=date_create($delete_account['date']);
                                $date2=date_create(date('Y-m-d'));
                                $diff=date_diff($date1,$date2);
                                $time_delete = intval($diff->format("%R%a"));
                                if($time_delete < 0) print $lang['time-until-deletion'].' '.($time_delete*(-1)).' '.$lang['days'];
                                else print $lang['time-to-deletion'];
                            ?>
                        </p>
                    </div>
                    <form action="" method="post" class="action-form">
                        <button type="submit" name="cancel-delete-account" class="action-button btn-info">
                            <span><?php print $lang['cancel-delete-account']; ?></span>
                            <i class="fas fa-undo"></i>
                        </button>
                    </form>
                </div>
                <?php } ?>
            </div>
        </div>
    </div>
</div>

<style>
/* Account Page - Modern Design (Inline per evitare conflitti) */
.account-page-modern { width: 100%; min-height: calc(100vh - 200px); }
.account-hero { background: linear-gradient(135deg, rgba(231, 76, 60, 0.1) 0%, rgba(192, 57, 43, 0.05) 100%); border: 1px solid rgba(231, 76, 60, 0.2); border-radius: 16px; padding: 50px 40px; text-align: center; margin-bottom: 40px; position: relative; overflow: hidden; }
.account-hero::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(231, 76, 60, 0.1) 0%, transparent 70%); animation: heroGlow 8s ease-in-out infinite; }
.account-hero-content { position: relative; z-index: 1; }
.account-hero .hero-icon { width: 90px; height: 90px; margin: 0 auto 25px; background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 30px rgba(231, 76, 60, 0.6); animation: heroIconFloat 3s ease-in-out infinite; }
.account-hero .hero-icon i { font-size: 42px; color: white; }
.account-title { font-family: var(--font-secondary); font-size: 38px; color: var(--color-primary); margin: 0 0 15px 0; text-transform: uppercase; letter-spacing: 2px; }
.account-subtitle { font-size: 18px; color: var(--color-text-dark); margin: 0; }
.account-subtitle strong { color: var(--color-primary); font-weight: 700; }
.account-container { max-width: 1200px; margin: 0 auto; }
.account-stats { display: grid; grid-template-columns: repeat(auto-fit, minmin(250px, 1fr)); gap: 20px; margin-bottom: 50px; }
.stat-card { background: var(--color-box-bg); backdrop-filter: blur(15px); border: 1px solid rgba(231, 76, 60, 0.15); border-radius: 12px; padding: 25px; display: flex; align-items: center; gap: 20px; transition: var(--transition-smooth); position: relative; overflow: hidden; }
.stat-card::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(231, 76, 60, 0.1), transparent); transition: left 0.6s; }
.stat-card:hover::before { left: 100%; }
.stat-card:hover { transform: translateY(-5px); border-color: rgba(231, 76, 60, 0.3); box-shadow: 0 8px 30px rgba(231, 76, 60, 0.3); }
.stat-icon { width: 60px; height: 60px; background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4); }
.stat-icon i { font-size: 28px; color: white; }
.stat-info { display: flex; flex-direction: column; gap: 5px; }
.stat-label { font-size: 13px; color: var(--color-text-dark); text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }
.stat-value { font-size: 24px; color: var(--color-text-light); font-weight: 700; }
.account-actions { background: var(--color-box-bg); backdrop-filter: blur(15px); border: 1px solid rgba(231, 76, 60, 0.15); border-radius: 16px; padding: 40px; box-shadow: var(--shadow-lg); }
.account-actions .section-title { font-family: var(--font-secondary); color: var(--color-primary); font-size: 24px; margin: 0 0 35px 0; display: flex; align-items: center; gap: 12px; text-transform: uppercase; padding-bottom: 20px; border-bottom: 2px solid rgba(231, 76, 60, 0.2); }
.action-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
.action-card { background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(231, 76, 60, 0.15); border-radius: 12px; padding: 25px; display: flex; flex-direction: column; gap: 15px; transition: var(--transition-smooth); position: relative; overflow: hidden; }
.action-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--color-primary); transform: scaleY(0); transition: transform 0.3s; }
.action-card:hover::before { transform: scaleY(1); }
.action-card:hover { transform: translateX(5px); border-color: rgba(231, 76, 60, 0.3); box-shadow: -5px 0 20px rgba(231, 76, 60, 0.2); }
.action-card.action-warning { border-color: rgba(241, 196, 15, 0.2); }
.action-card.action-warning::before { background: #F1C40F; }
.action-card.action-danger { border-color: rgba(231, 76, 60, 0.3); }
.action-card.action-info { border-color: rgba(52, 152, 219, 0.2); }
.action-card.action-info::before { background: #3498DB; }
.action-icon { width: 50px; height: 50px; background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.action-warning .action-icon { background: linear-gradient(135deg, #F1C40F 0%, #F39C12 100%); }
.action-danger .action-icon { background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%); }
.action-info .action-icon { background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%); }
.action-icon i { font-size: 24px; color: white; }
.action-content h4 { font-size: 18px; color: var(--color-text-light); margin: 0 0 8px 0; font-weight: 700; }
.action-content p { font-size: 14px; color: var(--color-text-dark); margin: 0; line-height: 1.5; }
.action-form { margin: 0; }
.action-button { display: flex; align-items: center; justify-content: space-between; width: 100%; padding: 12px 18px; background: rgba(231, 76, 60, 0.1); border: 1px solid rgba(231, 76, 60, 0.3); border-radius: 8px; color: var(--color-text-light); font-size: 14px; font-weight: 600; cursor: pointer; transition: var(--transition-smooth); }
.action-button:hover { background: rgba(231, 76, 60, 0.2); border-color: var(--color-primary); transform: translateX(3px); }
.action-button.btn-warning { background: rgba(241, 196, 15, 0.1); border-color: rgba(241, 196, 15, 0.3); }
.action-button.btn-warning:hover { background: rgba(241, 196, 15, 0.2); border-color: #F1C40F; }
.action-button.btn-danger { background: rgba(231, 76, 60, 0.15); border-color: rgba(231, 76, 60, 0.4); }
.action-button.btn-danger:hover { background: rgba(231, 76, 60, 0.3); border-color: #E74C3C; }
.action-button.btn-info { background: rgba(52, 152, 219, 0.1); border-color: rgba(52, 152, 219, 0.3); }
.action-button.btn-info:hover { background: rgba(52, 152, 219, 0.2); border-color: #3498DB; }
.action-button i { transition: transform 0.3s; }
.action-button:hover i { transform: translateX(3px); }
@media (max-width: 992px) { .account-stats { grid-template-columns: repeat(2, 1fr); } .action-grid { grid-template-columns: 1fr; } }
@media (max-width: 768px) { .account-hero { padding: 40px 20px; } .account-title { font-size: 28px; } .account-actions { padding: 25px 20px; } .account-stats { grid-template-columns: 1fr; } }
</style>
