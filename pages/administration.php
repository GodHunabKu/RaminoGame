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

            if($email_sent_successfully) {
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

                if($email_sent_successfully) {
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

            if($email_sent_successfully) {
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

            if($email_sent_successfully) {
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
