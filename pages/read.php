<div class="account-page-modern">
    <div class="account-hero">
        <div class="account-hero-content">
            <div class="hero-icon">
                <i class="fas fa-newspaper"></i>
            </div>
            <h1 class="account-title"><?php print htmlspecialchars($lang['news'], ENT_QUOTES, 'UTF-8'); ?></h1>
            <?php if($offline) print '<p class="account-subtitle" style="color: #E74C3C;"><strong>'.htmlspecialchars($lang['server-offline'], ENT_QUOTES, 'UTF-8').'</strong></p>'; ?>
        </div>
    </div>

    <div class="account-container">
        <?php
            if(!$offline && $database->is_loggedin())
                if($web_admin>=$jsondataPrivileges['news'])
                    include 'include/functions/edit-news.php';
        ?>

        <div class="page-content-box">
            <div style="background: var(--color-box-bg); border: 1px solid rgba(231, 76, 60, 0.15); border-radius: 12px; padding: 30px; box-shadow: var(--shadow-lg);">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; padding-bottom: 20px; border-bottom: 2px solid rgba(231, 76, 60, 0.2);">
                    <h2 style="font-family: var(--font-secondary); color: var(--color-primary); font-size: 28px; margin: 0;">
                        <?php print htmlspecialchars($article['title'], ENT_QUOTES, 'UTF-8'); ?>
                    </h2>
                    <?php
                        if(!$offline && $database->is_loggedin())
                            if($web_admin>=$jsondataPrivileges['news'])
                                print '<a href="'.$site_url.'?delete='.$read_id.'" onclick="return confirm(\''.htmlspecialchars($lang['sure?'], ENT_QUOTES, 'UTF-8').'\');" style="color: #E74C3C; font-size: 20px; transition: var(--transition-fast);">
                                          <i class="fas fa-trash"></i>
                                      </a>';
                    ?>
                </div>

                <div style="color: var(--color-text-light); font-size: 16px; line-height: 1.8; margin-bottom: 20px;">
                    <?php print $article['content']; ?>
                </div>

                <div style="display: flex; align-items: center; gap: 10px; color: var(--color-text-dark); font-size: 14px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
                    <i class="fas fa-calendar-alt"></i>
                    <span><?php print htmlspecialchars($article['time'], ENT_QUOTES, 'UTF-8'); ?></span>
                </div>
            </div>
        </div>
    </div>
</div>
