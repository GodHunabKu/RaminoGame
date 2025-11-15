<div class="account-page-modern">
    <div class="account-hero">
        <div class="account-hero-content">
            <div class="hero-icon">
                <i class="fas fa-user-friends"></i>
            </div>
            <h1 class="account-title"><?php print htmlspecialchars($lang['referrals'], ENT_QUOTES, 'UTF-8'); ?></h1>
            <p class="account-subtitle">Invita amici e ottieni ricompense</p>
        </div>
    </div>

    <div class="account-container">
        <div class="page-content-box">
            <div class="form-section">
                <h3 class="section-title">
                    <i class="fas fa-link"></i>
                    Il Tuo Link Referral
                </h3>
                <p style="color: var(--color-text-dark); margin-bottom: 20px;"><?php print htmlspecialchars($lang['referral-link'], ENT_QUOTES, 'UTF-8'); ?></p>

                <?php $link = $site_url.'users/register/'.$_SESSION['id']; ?>
                <div style="display: flex; gap: 10px;">
                    <input
                        type="text"
                        class="form-control-modern"
                        value="<?php print htmlspecialchars($link, ENT_QUOTES, 'UTF-8'); ?>"
                        id="share"
                        readonly
                        style="flex: 1;"
                    >
                    <button class="action-button" type="button" id="copyButton" onclick="copyReferralLink()" style="width: auto; padding: 15px 25px;">
                        <i class="fa fa-clipboard"></i>
                        <span>Copia</span>
                    </button>
                </div>
            </div>
        </div>

        <?php if(is_array($referrals_list) && count($referrals_list)) { ?>
        <div class="page-content-box" style="margin-top: 30px;">
            <div class="form-section">
                <h3 class="section-title">
                    <i class="fas fa-users"></i>
                    <?php print htmlspecialchars($lang['referral-invited'], ENT_QUOTES, 'UTF-8'); ?>
                </h3>

                <?php if($received) { ?>
                <div class="alert-modern alert-success">
                    <div class="alert-icon"><i class="fas fa-check-circle"></i></div>
                    <div class="alert-content">
                        <strong>Ricompensa Ricevuta!</strong>
                        <p>
                            <?php
                                print htmlspecialchars($lang['collected_md'], ENT_QUOTES, 'UTF-8').' '.$jsondataReferrals['coins'].' ';
                                if($jsondataReferrals['type']==1)
                                    print htmlspecialchars($lang['md'], ENT_QUOTES, 'UTF-8').' (MD)';
                                else
                                    print htmlspecialchars($lang['jd'], ENT_QUOTES, 'UTF-8').' (JD)';
                                print '.';
                            ?>
                        </p>
                    </div>
                    <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <?php } ?>

                <div style="overflow-x: auto;">
                    <table class="table table-dark table-striped">
                        <thead class="thead-inverse">
                            <tr>
                                <th>#</th>
                                <th><?php print htmlspecialchars($lang['char-name'], ENT_QUOTES, 'UTF-8'); ?></th>
                                <th><?php print htmlspecialchars($lang['level'], ENT_QUOTES, 'UTF-8'); ?></th>
                                <th><?php print htmlspecialchars($lang['play-time'], ENT_QUOTES, 'UTF-8'); ?></th>
                                <th><?php print htmlspecialchars($lang['collect'], ENT_QUOTES, 'UTF-8'); ?></th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php
                                $x=0;
                                $i=1;
                                foreach($referrals_list as $getChars) {

                                    $getCharsINFO = getPlayerInfo($getChars['registered']);

                                    if(count($getCharsINFO))
                                    {
                                        $hours = floor($getCharsINFO['playtime'] / 60);
                                        $minutes = $getCharsINFO['playtime'] % 60;

                                        echo'<tr>
                                              <td>'.$i++.'</td>
                                              <td>'.htmlspecialchars($getCharsINFO['name'], ENT_QUOTES, 'UTF-8').'</td>
                                              <td>'.$getCharsINFO['level'].'</td>
                                              <td>'.$hours.' ore & '.$minutes.' minuti</td>';
                                        if($getChars['claimed']==1) echo '<td><button class="btn btn-primary btn-sm disabled">'.htmlspecialchars($lang['collected'], ENT_QUOTES, 'UTF-8').'</button></td>';
                                        else {
                                        if($jsondataReferrals['hours']<=$hours && $jsondataReferrals['level']<=$getCharsINFO['level'])
                                            echo '<td><form action="" method="post"><input type="hidden" name="id" value="'.$getChars['registered'].'"><input id="submitBtn" type="submit" name="login" value="'.htmlspecialchars($lang['collect'], ENT_QUOTES, 'UTF-8').'" class="btn btn-primary btn-sm"/></td></form>';
                                        else echo '<td><button class="btn btn-primary btn-sm disabled">'.htmlspecialchars($lang['not_yet'], ENT_QUOTES, 'UTF-8').'</button></td>';}
                                        echo'</tr>';
                                          $x++;

                                    }
                                }
                            ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="alert-modern alert-info" style="margin-top: 30px;">
            <div class="alert-icon"><i class="fas fa-info-circle"></i></div>
            <div class="alert-content">
                <strong>Requisiti per Ricompensa</strong>
                <p>
                    <i class="fas fa-clock"></i> <?php print htmlspecialchars($lang['referral-min-hours'], ENT_QUOTES, 'UTF-8').': '.$jsondataReferrals['hours']; ?><br>
                    <i class="fas fa-star"></i> <?php print htmlspecialchars($lang['referral-min-level'], ENT_QUOTES, 'UTF-8').': '.$jsondataReferrals['level']; ?>
                </p>
            </div>
        </div>
        <?php } ?>
    </div>
</div>

<script>
function copyReferralLink() {
    const copyText = document.getElementById("share");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");

    const button = document.getElementById("copyButton");
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check"></i> <span>Copiato!</span>';
    button.style.background = 'rgba(39, 174, 96, 0.2)';
    button.style.borderColor = '#27AE60';

    setTimeout(function() {
        button.innerHTML = originalHTML;
        button.style.background = '';
        button.style.borderColor = '';
    }, 2000);
}
</script>
