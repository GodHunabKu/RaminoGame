<div class="account-page-modern">
    <div class="account-hero">
        <div class="account-hero-content">
            <div class="hero-icon">
                <i class="fas fa-donate"></i>
            </div>
            <h1 class="account-title"><?php print htmlspecialchars($lang['donate'], ENT_QUOTES, 'UTF-8'); ?></h1>
            <p class="account-subtitle">Supporta il server e ottieni ricompense esclusive</p>
        </div>
    </div>

    <div class="account-container">
        <?php
        if(isset($_POST['id']) && isset($_POST['type']) && isset($_POST['code']) && strlen($_POST['code']) >= 3 && strlen($_POST['code']) <= 50)
        {
            if(isset($jsondataDonate[$_POST['id']]['list'][$_POST['type']]))
            {
                $price = $jsondataDonate[$_POST['id']]['list'][$_POST['type']];
                $type = $jsondataDonate[$_POST['id']]['name'].' ['.$price['price'].' '.$jsondataCurrency[$price['currency']]['name'].' - '.$price['md'].' MD]';

                insert_donate($_SESSION['id'], $_POST['code'], $type);

                print '<div class="alert-modern alert-success">
                          <div class="alert-icon"><i class="fas fa-check-circle"></i></div>
                          <div class="alert-content">
                              <strong>Successo!</strong>
                              <p>'.htmlspecialchars($lang['send-donate'], ENT_QUOTES, 'UTF-8').'</p>
                          </div>
                          <button type="button" class="alert-close" onclick="this.parentElement.remove()">
                              <i class="fas fa-times"></i>
                          </button>
                      </div>';
            }
        }

        if(count($jsondataDonate)) { ?>

        <div class="action-grid">
            <?php $i=-1; foreach($jsondataDonate as $key => $donate) { $i++; ?>
            <div class="action-card">
                <div class="action-icon">
                    <i class="fas fa-<?php if(strtolower($donate['name'])=="paypal") print 'paypal fab'; else print 'credit-card'; ?>"></i>
                </div>
                <div class="action-content">
                    <h4><?php print htmlspecialchars($donate['name'], ENT_QUOTES, 'UTF-8'); ?></h4>
                    <p>Scegli il metodo di donazione e l'importo</p>
                </div>

                <?php if(strtolower($donate['name'])=="paypal") { ?>
                <form action="" method="post" class="action-form" style="width: 100%;">
                    <input type="hidden" name="id" value="<?php print $i; ?>">
                    <input type="hidden" name="method" value="<?php print htmlspecialchars($donate['name'], ENT_QUOTES, 'UTF-8'); ?>">
                    <div class="form-group-modern">
                        <label>
                            <i class="fas fa-dollar-sign"></i>
                            Seleziona Importo
                        </label>
                        <select class="form-control-modern" name="type" style="margin-bottom: 10px;">
                        <?php $j=-1; foreach($jsondataDonate[$i]['list'] as $key => $price) { $j++; ?>
                            <option value="<?php print $j; ?>"><?php print htmlspecialchars($lang['price'], ENT_QUOTES, 'UTF-8').' '.$price['price'].' '.$jsondataCurrency[$price['currency']]['name'].' - '.$price['md'].' MD'; ?></option>
                        <?php } ?>
                        </select>
                    </div>
                    <button type="submit" name="submit" class="action-button">
                        <span><?php print htmlspecialchars($lang['send'], ENT_QUOTES, 'UTF-8'); ?></span>
                        <i class="fas fa-arrow-right"></i>
                    </button>
                </form>
                <?php } else { ?>
                <form action="" method="post" class="action-form" style="width: 100%;">
                    <input type="hidden" name="id" value="<?php print $i; ?>">
                    <input type="hidden" name="method" value="<?php print htmlspecialchars($donate['name'], ENT_QUOTES, 'UTF-8'); ?>">
                    <div class="form-group-modern">
                        <label>
                            <i class="fas fa-dollar-sign"></i>
                            Seleziona Importo
                        </label>
                        <select class="form-control-modern" name="type" style="margin-bottom: 10px;">
                        <?php $j=-1; foreach($jsondataDonate[$i]['list'] as $key => $price) { $j++; ?>
                            <option value="<?php print $j; ?>"><?php print htmlspecialchars($lang['price'], ENT_QUOTES, 'UTF-8').' '.$price['price'].' '.$jsondataCurrency[$price['currency']]['name'].' - '.$price['md'].' MD'; ?></option>
                        <?php } ?>
                        </select>
                    </div>
                    <div class="form-group-modern">
                        <label>
                            <i class="fas fa-ticket-alt"></i>
                            Codice Transazione
                        </label>
                        <input type="text" class="form-control-modern" maxlength="50" name="code" placeholder="<?php print htmlspecialchars($lang['code'], ENT_QUOTES, 'UTF-8'); ?>" required>
                        <div class="input-border"></div>
                    </div>
                    <button type="submit" name="submit" class="action-button">
                        <span><?php print htmlspecialchars($lang['send'], ENT_QUOTES, 'UTF-8'); ?></span>
                        <i class="fas fa-arrow-right"></i>
                    </button>
                </form>
                <?php } ?>
            </div>
            <?php } ?>
        </div>

        <?php } else { ?>
        <div class="alert-modern alert-info">
            <div class="alert-icon"><i class="fas fa-info-circle"></i></div>
            <div class="alert-content">
                <strong>Informazione</strong>
                <p>Nessun metodo di donazione disponibile al momento.</p>
            </div>
        </div>
        <?php } ?>
    </div>
</div>
