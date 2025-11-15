<div class="account-page-modern">
    <div class="account-hero">
        <div class="account-hero-content">
            <div class="hero-icon">
                <i class="fas fa-vote-yea"></i>
            </div>
            <h1 class="account-title"><?php print htmlspecialchars($lang['vote'], ENT_QUOTES, 'UTF-8'); ?></h1>
            <p class="account-subtitle">Vota per il server e guadagna MD/JD</p>
        </div>
    </div>

    <div class="account-container">
        <?php if(isset($voted_now) && isset($already_voted) && !$voted_now) { ?>
        <div class="alert-modern alert-danger">
            <div class="alert-icon"><i class="fas fa-exclamation-circle"></i></div>
            <div class="alert-content">
                <strong>Attenzione!</strong>
                <p><?php print htmlspecialchars($lang['vote-again'], ENT_QUOTES, 'UTF-8').' <strong>'.$already_voted.'</strong>'; ?></p>
            </div>
            <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <?php } ?>

        <?php if(count($vote4coins)) { ?>
        <div class="page-content-box">
            <div style="overflow-x: auto;">
                <table class="table table-dark table-striped">
                    <thead class="thead-inverse">
                        <tr>
                            <th style="width: 10%">#</th>
                            <th style="width: 30%">Sito</th>
                            <th style="width: 20%"><?php print htmlspecialchars($lang['value'], ENT_QUOTES, 'UTF-8'); ?></th>
                            <th style="width: 20%"><?php print htmlspecialchars($lang['time'], ENT_QUOTES, 'UTF-8'); ?></th>
                            <th style="width: 20%"><?php print htmlspecialchars($lang['vote'], ENT_QUOTES, 'UTF-8'); ?></th>
                        </tr>
                    </thead>
                    <tbody>
                    <?php $i=1; foreach($vote4coins as $key => $vote) { ?>
                        <tr>
                            <th scope="row"><?php print $i++; ?></th>
                            <td><?php print htmlspecialchars($vote['name'], ENT_QUOTES, 'UTF-8'); ?></td>
                            <td>
                                <span style="color: var(--color-primary); font-weight: 700; font-size: 16px;">
                                    <?php print $vote['value']; if($vote['type']==1) print ' MD'; else print ' JD'; ?>
                                </span>
                            </td>
                            <td><?php print $vote['time'].' '.htmlspecialchars($lang['hours'], ENT_QUOTES, 'UTF-8'); ?></td>
                            <td>
                                <a href="<?php print $site_url.'user/vote4coins/'.$key; ?>" class="action-button" style="display: inline-flex; width: auto; padding: 10px 20px;">
                                    <span><?php print htmlspecialchars($lang['vote'], ENT_QUOTES, 'UTF-8'); ?></span>
                                    <i class="fas fa-external-link-alt"></i>
                                </a>
                            </td>
                        </tr>
                    <?php } ?>
                    </tbody>
                </table>
            </div>
        </div>
        <?php } else { ?>
        <div class="alert-modern alert-info">
            <div class="alert-icon"><i class="fas fa-info-circle"></i></div>
            <div class="alert-content">
                <strong>Informazione</strong>
                <p><?php print htmlspecialchars($lang['no-download-links'], ENT_QUOTES, 'UTF-8'); ?></p>
            </div>
        </div>
        <?php } ?>
    </div>
</div>
