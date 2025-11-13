<?php
	$list = characters_list();
	$ranking = get_player_rank($list);
?>
<div class="account-page-modern">
    <div class="account-hero">
        <div class="account-hero-content">
            <div class="hero-icon">
                <i class="fas fa-users"></i>
            </div>
            <h1 class="account-title">I Tuoi Personaggi</h1>
            <?php $account_name = getAccountName($_SESSION['id']); ?>
            <p class="account-subtitle">Account: <strong><?php echo htmlspecialchars($account_name, ENT_QUOTES, 'UTF-8'); ?></strong></p>
        </div>
    </div>

    <div class="page-content-box">
        <?php
            if($jsondataFunctions['players-debug'] && isset($_POST['debug']))
                foreach($list as $player)
                    if($player['id']==intval($_POST['debug']))
                    {
                        print '<div class="alert-modern alert-success">
                                  <div class="alert-icon"><i class="fas fa-check-circle"></i></div>
                                  <div class="alert-content">
                                      <strong>Successo!</strong>
                                      <p>'.htmlspecialchars($lang['debug-success'], ENT_QUOTES, 'UTF-8').'</p>
                                  </div>
                                  <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                                      <i class="fas fa-times"></i>
                                  </button>
                              </div>';

                        $empire = get_player_empire($_SESSION['id']);

                        if($empire==1) { $mapindex = "0"; $x = "459770"; $y = "953980";}
                        elseif($empire==2) { $mapindex = "21"; $x = "52043"; $y = "166304";}
                        elseif($empire==3) { $mapindex = "41"; $x = "957291"; $y = "255221";}

                        reset_char($player['id'], $mapindex, $x, $y);
                    }
        ?>

        <?php if(count($list)) { ?>
        <div style="overflow-x: auto;">
            <table class="table table-dark table-striped">
                <thead class="thead-inverse">
                    <tr>
                        <th>#</th>
                        <th><?php print htmlspecialchars($lang['class'], ENT_QUOTES, 'UTF-8'); ?></th>
                        <th><?php print htmlspecialchars($lang['name'], ENT_QUOTES, 'UTF-8'); ?></th>
                        <th><?php print htmlspecialchars($lang['level'], ENT_QUOTES, 'UTF-8'); ?></th>
                        <th>EXP</th>
                        <?php if($jsondataFunctions['players-debug']) { ?>
                            <th><?php print htmlspecialchars($lang['debug'], ENT_QUOTES, 'UTF-8'); ?></th>
                        <?php } ?>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach($list as $player) {
                        $job = job_name($player['job']);
                    ?>
                    <tr>
                        <th scope="row"><?php print $ranking[$player['name']]; ?></th>
                        <td><img src="<?php print $site_url.'images/job/'.$player['job'].'.png'; ?>" width="32" alt="<?php print htmlspecialchars($job, ENT_QUOTES, 'UTF-8'); ?>" title="<?php print htmlspecialchars($job, ENT_QUOTES, 'UTF-8'); ?>"></td>
                        <td><?php print htmlspecialchars($player['name'], ENT_QUOTES, 'UTF-8'); ?></td>
                        <td><?php print $player['level']; ?></td>
                        <td><?php print number_format($player['exp']); ?></td>
                        <?php if($jsondataFunctions['players-debug']) { ?>
                            <td>
                                <form action="" method="post">
                                    <input type="hidden" name="debug" value="<?php print $player['id']; ?>">
                                    <button type="submit" name="submit" class="btn btn-primary btn-sm"><?php print htmlspecialchars($lang['debug'], ENT_QUOTES, 'UTF-8'); ?></button>
                                </form>
                            </td>
                        <?php } ?>
                    </tr>
                    <?php } ?>
                </tbody>
            </table>
        </div>
        <?php } else { ?>
        <div class="alert-modern alert-info">
            <div class="alert-icon"><i class="fas fa-info-circle"></i></div>
            <div class="alert-content">
                <strong>Informazione</strong>
                <p><?php print htmlspecialchars($lang['no-chars'], ENT_QUOTES, 'UTF-8'); ?></p>
            </div>
        </div>
        <?php } ?>
    </div>
</div>
