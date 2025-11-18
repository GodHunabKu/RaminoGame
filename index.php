<?php
// ===== SICUREZZA: Logging Visite con controlli migliorati =====
function logVisita() {
    // Controllo sicuro dell'IP
    $ip = isset($_SERVER['REMOTE_ADDR']) ? filter_var($_SERVER['REMOTE_ADDR'], FILTER_VALIDATE_IP) : 'UNKNOWN';
    if (!$ip) $ip = 'IP_NON_VALIDO';
    
    $data = date("Y-m-d H:i:s");
    
    // Controllo sicuro dello User Agent
    $user_agent = isset($_SERVER['HTTP_USER_AGENT']) ? htmlspecialchars($_SERVER['HTTP_USER_AGENT'], ENT_QUOTES, 'UTF-8') : 'Unknown Browser';
    
    $logFile = 'visite.txt';
    $log = "[$data] IP: $ip | Agent: $user_agent\n";
    
    // Limita il file di log a 1000 righe
    if (file_exists($logFile)) {
        $lines = file($logFile);
        if (count($lines) > 1000) {
            $lines = array_slice($lines, -1000);
            file_put_contents($logFile, implode('', $lines));
        }
    }
    
    @file_put_contents($logFile, $log, FILE_APPEND | LOCK_EX);
}
logVisita();

@ob_start();
include 'include/functions/header.php';

// ===================================================================
// Logica affidabile per rilevare la Homepage
// ===================================================================
$is_homepage = false;
$request_uri = strtok($_SERVER["REQUEST_URI"], '?'); 
$site_path = rtrim(parse_url($site_url, PHP_URL_PATH), '/');

if (empty($site_path)) {
    $site_path = '/';
}

if ($request_uri == $site_path || $request_uri == $site_path . '/' || $request_uri == $site_path . '/index.php') {
    $is_homepage = true;
}
// ===================================================================

// Logica per l'URL dell'Item Shop
if(isset($item_shop) && $item_shop != "") {
    $shop_url = $item_shop;
} else if(is_dir('shop')) {
    $shop_url = $site_url . 'shop';
} else {
    $shop_url = '#';
}
?>
<!DOCTYPE html>
<html lang="<?php print $language_code; ?>"<?php if(in_array($language_code, $rtl)) print ' dir="rtl"'; ?>>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title><?php print $site_title.' - '.$title; if($offline) print ' - '.$lang['server-offline']; ?></title>

    <!-- SEO Meta Tags -->
    <meta name="description" content="ONE: Il nuovo server Metin2 italiano con livello max 220, gameplay FULL NEWSTYLE e oltre 1000 personalizzazioni. Shop 100% in-game!">
    <meta name="keywords" content="metin2, server metin2, metin2 italiano, ONE server, newstyle, mmorpg, metin2 privato, server privato metin2">
    <meta name="author" content="ONE Server">
    <meta name="robots" content="index, follow">
    <meta name="language" content="Italian">
    <meta name="revisit-after" content="7 days">

    <!-- Open Graph / Facebook / Discord -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="<?php echo $site_url; ?>">
    <meta property="og:title" content="<?php print $site_title.' - '.$title; ?>">
    <meta property="og:description" content="ONE: Il nuovo server Metin2 italiano con livello max 220, gameplay FULL NEWSTYLE e oltre 1000 personalizzazioni. Shop 100% in-game!">
    <meta property="og:image" content="<?php echo $site_url; ?>images/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:site_name" content="<?php print $site_title; ?>">
    <meta property="og:locale" content="it_IT">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="<?php echo $site_url; ?>">
    <meta name="twitter:title" content="<?php print $site_title.' - '.$title; ?>">
    <meta name="twitter:description" content="ONE: Il nuovo server Metin2 italiano con livello max 220, gameplay FULL NEWSTYLE e oltre 1000 personalizzazioni. Shop 100% in-game!">
    <meta name="twitter:image" content="<?php echo $site_url; ?>images/og-image.png">

    <!-- Canonical URL -->
    <link rel="canonical" href="<?php echo $site_url; ?>">

    <!-- Theme Color -->
    <meta name="theme-color" content="#E74C3C">
    <meta name="msapplication-TileColor" content="#E74C3C">

    <!-- Apple Touch Icon -->
    <link rel="apple-touch-icon" sizes="180x180" href="<?php echo $site_url; ?>images/apple-touch-icon.png">
    
    <!-- Preconnect -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://cdn.jsdelivr.net">
    
    <!-- Font -->
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />

    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">

    <!-- CSS Principale -->
    <link rel="stylesheet" href="<?php echo $site_url; ?>css/styles.css?v=<?php echo time(); ?>" type="text/css">
    <link rel="stylesheet" href="<?php echo $site_url; ?>css/alert-modern.css?v=<?php echo time(); ?>" type="text/css">
<?php if($page == 'ranking/players' || $page == 'ranking/guilds') { ?>
<link rel="stylesheet" href="<?php echo $site_url; ?>css/ranking-animations.css?v=<?php echo time(); ?>">
<?php } ?>
<?php if($page == 'ranking/players' || $page == 'ranking/guilds') { ?>
<link rel="stylesheet" href="<?php echo $site_url; ?>css/ranking-advanced.css?v=<?php echo time(); ?>">
<?php } ?>

    <?php if($page != 'admin') { ?>
    <!-- Modern Design System (escluso dal pannello admin) -->
    <link rel="stylesheet" href="<?php echo $site_url; ?>css/variables.css?v=<?php echo time(); ?>" type="text/css">
    <?php } ?>

    <!-- Sidebar Gold Button (ItemShop Premium) -->
    <link rel="stylesheet" href="<?php echo $site_url; ?>css/sidebar-gold-button.css?v=<?php echo time(); ?>" type="text/css">

    <?php if($is_homepage) { ?>
    <!-- Homepage Premium 2025 - Solo Homepage -->
    <link rel="stylesheet" href="<?php echo $site_url; ?>css/homepage-premium.css?v=<?php echo time(); ?>" type="text/css">
    <?php } ?>

    <!-- Favicon -->
    <link rel="shortcut icon" href="<?php echo $site_url; ?>kebab/logo3.png">
    
    <!-- reCAPTCHA -->
    <script src="https://www.google.com/recaptcha/api.js" async defer></script>

    <?php if($page == 'admin') { ?>
    <!-- Admin Panel Styles -->
    <link rel="stylesheet" href="<?php echo $site_url; ?>css/admin.css?v=<?php echo time(); ?>" type="text/css">
    <?php } ?>
</head>
<body class="<?php if($is_homepage) echo 'homepage-style'; if($page == 'admin') echo ' admin-page'; ?>">

    <?php if($page != 'admin') { ?>
    <!-- ====================================
         SFONDO ANIMATO (escluso dal pannello admin)
         ==================================== -->
    <div class="animated-bg">
        <div class="bg-gradient"></div>
        <div class="particles"></div>
        <div class="bg-glow"></div>
    </div>
    <div class="background-fog"></div>

    <div id="preloader"></div>
    <?php } ?>

    <div class="page-wrapper">

        <!-- ====================================
             HEADER - SEMPRE VISIBILE
             ==================================== -->
        <header class="main-header">
            <a href="<?php echo $site_url; ?>" class="nav-logo" aria-label="Homepage ONE">
                <img src="<?php echo $site_url; ?>kebab/logo3.png" alt="<?php echo $site_title; ?> Logo">
            </a>
            <nav class="main-nav" aria-label="Navigazione principale">
                <a href="<?php echo $site_url; ?>news/"><?php echo $lang['news']; ?></a>
                <a href="<?php echo $site_url; ?>download"><?php echo $lang['download']; ?></a>
                <?php if(!$database->is_loggedin()) { ?>
                <a href="<?php echo $site_url; ?>users/register"><?php echo $lang['register']; ?></a>
                <?php } else { ?>
                <a href="<?php echo $site_url; ?>user/administration"><?php echo $lang['account-data']; ?></a>
                <?php } ?>
                <a href="<?php echo $site_url; ?>ranking/players"><?php echo $lang['ranking']; ?></a>
            </nav>
            <div class="user-area">
                <div class="user-actions">
                    <?php if($offline || !$database->is_loggedin()) { ?>
                        <a href="<?php echo $site_url; ?>users/login"><span><?php echo $lang['login']; ?></span>Login</a>
                    <?php } else { ?>
                        <a href="<?php echo $site_url; ?>user/administration"><span>Benvenuto/a</span><?php echo htmlspecialchars(getAccountName($_SESSION['id']), ENT_QUOTES, 'UTF-8'); ?></a>
                    <?php } ?>
                </div>
                <div class="dropdown">
                    <button class="dropbtn" aria-haspopup="true" aria-expanded="false"><i class="fas fa-user-circle"></i> User <i class="fas fa-caret-down"></i></button>
                    <div class="dropdown-content" role="menu">
                        <?php if($offline || !$database->is_loggedin()) { ?>
                            <a href="<?php echo $site_url; ?>users/login" role="menuitem"><?php echo $lang['login']; ?></a>
                            <a href="<?php echo $site_url; ?>users/register" role="menuitem"><?php echo $lang['register']; ?></a>
                        <?php } else { ?>
                            <a href="<?php echo $site_url; ?>user/administration" role="menuitem"><?php echo $lang['account-data']; ?></a>
                            <a href="<?php echo $site_url; ?>user/characters" role="menuitem"><?php echo $lang['chars-list']; ?></a>
                            <a href="<?php echo $site_url; ?>users/logout" role="menuitem"><?php echo $lang['logout']; ?></a>
                        <?php } ?>
                    </div>
                </div>
                <a href="<?php echo $site_url; ?>download" class="btn-download"><i class="fas fa-download"></i> Download</a>
            </div>
            <button id="mobile-menu-toggle" aria-label="Menu" aria-expanded="false"><i class="fas fa-bars"></i></button>
        </header>

        <div class="main-container">
            
            <!-- ====================================
                 SIDEBAR SINISTRA
                 ==================================== -->
            <aside class="sidebar" role="navigation" aria-label="Menu laterale">
                <nav class="sidebar-nav">
                    <ul>
                        <li class="active"><a href="<?php echo $site_url; ?>"><i class="fas fa-home"></i> Homepage</a></li>
                        <li><a href="<?php echo $site_url; ?>news/"><i class="fas fa-newspaper"></i> <?php echo $lang['news']; ?></a></li>
                        <li><a href="<?php echo $site_url; ?>ranking/players"><i class="fas fa-trophy"></i> <?php echo $lang['ranking']; ?></a></li>
                        <li><a href="<?php echo $site_url; ?>download"><i class="fas fa-download"></i> <?php echo $lang['download']; ?></a></li>
                        <li><a href="<?php echo $site_url; ?>users/register"><i class="fas fa-user-plus"></i> <?php echo $lang['register']; ?></a></li>
                        <?php if($shop_url && $shop_url != '#') { ?>
                        <li class="itemshop-premium">
                            <a href="<?php print $shop_url; ?>" target="_blank">
                                <i class="fas fa-shopping-cart"></i> <?php echo $lang['item-shop']; ?>
                                <span class="badge-hot">HOT</span>
                            </a>
                            <span class="sparkle"></span>
                            <span class="sparkle"></span>
                            <span class="sparkle"></span>
                            <span class="sparkle"></span>
                        </li>
                        <?php } ?>
                        <?php if(isset($social_links['discord']) && $social_links['discord']) { ?>
                        <li><a href="<?php print $social_links['discord']; ?>" target="_blank"><i class="fab fa-discord"></i> Discord</a></li>
                        <?php } ?>
                    </ul>
                </nav>
            </aside>

            <!-- ====================================
                 CONTENUTO CENTRALE
                 ==================================== -->
            <main class="content-area">
                <?php if ($is_homepage) : ?>
                
                <!-- HERO SECTION -->
                <section class="hero-section">
                    <!-- LOGO CON STATS AI LATI -->
                    <div class="hero-top-section">
                        <?php if($jsondataFunctions['players-online']) { ?>
                        <div class="stat-box stat-left">
                            <div class="stat-icon"><i class="fas fa-users"></i></div>
                            <div class="stat-info">
                                <h4><?php print number_format($loaded_stats['players-online'], 0, '', ','); ?></h4>
                                <p><?php print $lang['players-online']; ?></p>
                            </div>
                        </div>
                        <?php } ?>
                        
                        <div class="hero-logo">
                            <img src="<?php echo $site_url; ?>kebab/logo3.png" alt="<?php echo $site_title; ?> Logo">
                        </div>
                        
                        <?php if($jsondataFunctions['players-online-last-24h']) { ?>
                        <div class="stat-box stat-right">
                            <div class="stat-icon"><i class="fas fa-clock"></i></div>
                            <div class="stat-info">
                                <h4><?php print number_format($loaded_stats['players-online-last-24h'], 0, '', '.'); ?></h4>
                                <p><?php print $lang['players-online']; ?> (24h)</p>
                            </div>
                        </div>
                        <?php } ?>
                    </div>
                    
                    <p class="hero-tagline">Forgia il tuo destino, conquista la vetta!</p>
                    
                    <!-- TRAILER VIDEO -->
                    <div class="trailer-container">
                        <div class="trailer-badge">
                            <i class="fas fa-play-circle"></i>
                            <span>TRAILER UFFICIALE</span>
                        </div>
                        <div class="video-wrapper">
                            <iframe 
                                src="https://player.vimeo.com/video/1133246945?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" 
                                title="ONE Server - Trailer Ufficiale" 
                                frameborder="0" 
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                allowfullscreen
                            ></iframe>
                        </div>
                        <div class="trailer-info">
                            <div class="info-item">
                                <i class="fas fa-film"></i>
                                <span>Gameplay Epico</span>
                            </div>
                            <div class="info-item">
                                <i class="fas fa-star"></i>
                                <span>Grafica Mozzafiato</span>
                            </div>
                            <div class="info-item">
                                <i class="fas fa-fire"></i>
                                <span>Azione Intensa</span>
                            </div>
                        </div>
                    </div>

                    <!-- CTA BUTTONS -->
                    <div class="hero-cta-buttons">
                        <a href="<?php echo $site_url; ?>download" class="cta-button cta-primary">
                            <i class="fas fa-download"></i>
                            <span class="cta-text">
                                <strong>SCARICA IL CLIENT</strong>
                                <small>Inizia la tua avventura</small>
                            </span>
                        </a>
                        <?php if(!$database->is_loggedin()) { ?>
                        <a href="<?php echo $site_url; ?>users/register" class="cta-button cta-secondary">
                            <i class="fas fa-user-plus"></i>
                            <span class="cta-text">
                                <strong>REGISTRATI ORA</strong>
                                <small>Gratis e senza limiti</small>
                            </span>
                        </a>
                        <?php } else { ?>
                        <a href="<?php echo $site_url; ?>user/administration" class="cta-button cta-secondary">
                            <i class="fas fa-user-circle"></i>
                            <span class="cta-text">
                                <strong>IL MIO ACCOUNT</strong>
                                <small>Gestisci il tuo profilo</small>
                            </span>
                        </a>
                        <?php } ?>
                    </div>
                </section>

                <!-- CONTENT GRID: 3 BOX -->
                <div class="content-grid">
                    
                    <?php if(!$offline && $statistics) { ?>
                    <!-- BOX STATISTICHE -->
                    <section class="content-box stats-box">
                        <h3><i class="fas fa-chart-bar"></i> <?php print $lang['statistics']; ?></h3>
                        <div class="stats-table">
                            <table>
                                <tbody>
                                    <?php foreach($jsondataFunctions as $key => $status) {
                                        if(!in_array($key, ['active-registrations', 'players-debug', 'active-referrals', 'full-news-text']) && $status) { ?>
                                    <tr>
                                        <td>&bull; <?php if($key!='players-online-last-24h') print $lang[$key]; else print str_replace("(24h)", '<span class="highlight">(24h)</span>', $lang[$key]); ?></td>
                                        <td><?php print number_format($loaded_stats[$key], 0, '', ' '); ?></td>
                                    </tr>
                                    <?php } } ?>
                                </tbody>
                            </table>
                        </div>
                        <div class="stats-update">
                            <i class="fas fa-sync-alt"></i> 
                            <a href="" class="reload-button">Last update: <span><?php print time_elapsed_string($last_modified_time_stats, true); ?></span></a>
                        </div>
                    </section>
                    <?php } ?>
                    
                    <?php if(!$offline && !empty($jsondataRanking['top10backup']['players'])) { ?>
                    <!-- BOX GIOCATORI -->
                    <section class="content-box ranking-box">
                        <h3><i class="fas fa-trophy"></i> <?php print $lang['players']; ?></h3>
                        
                        <div class="top-player-featured">
                            <div class="featured-badge">
                                <img src="<?php print $site_url; ?>images/top1.png" alt="Gold">
                            </div>
                            <div class="featured-image">
                                <img src="<?php print $site_url.'images/job/'.$jsondataRanking['top10backup']['players'][0]['job']; ?>.png" alt="">
                            </div>
                            <div class="featured-info">
                                <h4>
                                    <?php print $jsondataRanking['top10backup']['players'][0]['name']; ?>
                                    <span class="emp-<?php print $jsondataRanking['top10backup']['players'][0]['empire']; ?>">
                                        [<?php print empire_name($jsondataRanking['top10backup']['players'][0]['empire']); ?>]
                                    </span>
                                </h4>
                                <p>Lvl. <strong><?php print $jsondataRanking['top10backup']['players'][0]['level']; ?></strong></p>
                            </div>
                        </div>
                        
                        <div class="ranking-table">
                            <table>
                                <tbody>
                                    <?php $i=0; foreach($jsondataRanking['top10backup']['players'] as $player) { 
                                        $i++; 
                                        if($i==1) continue; 
                                    ?>
                                    <tr>
                                        <td class="rank-col">
                                            <?php 
                                            if($i==2) print '<img src="'.$site_url.'images/top2.png" alt="Silver" />'; 
                                            else if($i==3) print '<img src="'.$site_url.'images/top3.png" alt="Bronze" />'; 
                                            else print '<span class="rank-number">'.$i.'</span>'; 
                                            ?>
                                        </td>
                                        <td><?php print $player['name']; ?></td>
                                        <td>Lvl. <?php print $player['level']; ?></td>
                                    </tr>
                                    <?php } ?>
                                </tbody>
                            </table>
                        </div>
                        
                        <a href="<?php print $site_url; ?>ranking/players" class="btn-more">
                            Top 100 <i class="fas fa-arrow-right"></i>
                        </a>
                    </section>
                    <?php } ?>
                    
                    <?php if(!$offline && !empty($jsondataRanking['top10backup']['guilds'])) { ?>
                    <!-- BOX GILDE -->
                    <section class="content-box ranking-box">
                        <h3><i class="fas fa-shield-alt"></i> <?php print $lang['guilds']; ?></h3>
                        
                        <div class="top-player-featured">
                            <div class="featured-badge">
                                <img src="<?php print $site_url; ?>images/top1.png" alt="Gold">
                            </div>
                            <div class="featured-image">
                                <img src="<?php print $site_url.'images/job/'.$jsondataRanking['top10backup']['guilds'][0]['master_job']; ?>.png" alt="">
                            </div>
                            <div class="featured-info">
                                <h4>
                                    <?php print $jsondataRanking['top10backup']['guilds'][0]['name']; ?>
                                    <span class="emp-<?php print $jsondataRanking['top10backup']['guilds'][0]['empire']; ?>">
                                        [<?php print empire_name($jsondataRanking['top10backup']['guilds'][0]['empire']); ?>]
                                    </span>
                                </h4>
                                <p>Points: <strong><?php print $jsondataRanking['top10backup']['guilds'][0]['ladder_point']; ?></strong></p>
                            </div>
                        </div>
                        
                        <div class="ranking-table">
                            <table>
                                <tbody>
                                    <?php $i=0; foreach($jsondataRanking['top10backup']['guilds'] as $guild) { 
                                        $i++; 
                                        if($i==1) continue; 
                                    ?>
                                    <tr>
                                        <td class="rank-col">
                                            <?php 
                                            if($i==2) print '<img src="'.$site_url.'images/top2.png" alt="Silver" />'; 
                                            else if($i==3) print '<img src="'.$site_url.'images/top3.png" alt="Bronze" />'; 
                                            else print '<span class="rank-number">'.$i.'</span>'; 
                                            ?>
                                        </td>
                                        <td><?php print $guild['name']; ?></td>
                                        <td><?php print number_format($guild['ladder_point'], 0, '', '.'); ?></td>
                                    </tr>
                                    <?php } ?>
                                </tbody>
                            </table>
                        </div>
                        
                        <a href="<?php print $site_url; ?>ranking/guilds" class="btn-more">
                            Top 100 <i class="fas fa-arrow-right"></i>
                        </a>
                    </section>
                    <?php } ?>
                    
                </div>
                
                <?php else: ?>
                    <!-- ALTRE PAGINE -->
                    <section class="content-box page-content-box">
                        <?php include 'pages/'.$page.'.php'; ?>
                    </section>
                <?php endif; ?>
            </main>

            <!-- ====================================
                 SIDEBAR DESTRA (LOGIN)
                 ==================================== -->
            <aside class="sidebar-right">
                <h3><i class="fas fa-sign-in-alt"></i> LOGIN</h3>
                
                <?php if($offline || !$database->is_loggedin()) { ?>
                <!-- FORM LOGIN -->
                <form method="post" action="<?php print $site_url; ?>users/login" class="login-form">
                    <div class="form-group">
                        <div class="input-icon"><i class="fas fa-user"></i></div>
                        <input name="username" type="text" placeholder="<?php print $lang['user-name-or-email']; ?>" required>
                    </div>
                    <div class="form-group">
                        <div class="input-icon"><i class="fas fa-lock"></i></div>
                        <input name="password" type="password" placeholder="<?php print $lang['password']; ?>" required>
                    </div>
                    <?php if(!$offline) { ?>
                    <div class="form-group">
                        <div class="recaptcha-wrapper">
                            <div class="g-recaptcha" data-sitekey="<?php print $site_key; ?>" data-theme="dark" data-size="compact"></div>
                        </div>
                    </div>
                    <?php } ?>
                    <div class="form-footer">
                        <a href="<?php print $site_url; ?>users/lost" class="forgot-link"><?php print $lang['forget-password']; ?></a>
                    </div>
                    <button type="submit" class="btn-submit">
                        <i class="fas fa-sign-in-alt"></i> LOG IN
                    </button>
                </form>
                
                <?php } else { ?>
                <!-- USER MENU (se loggato) -->
                <div class="user-menu">
                    <?php if($web_admin) { ?>
                    <a href="<?php print $site_url; ?>admin">
                        <i class="fas fa-cogs"></i> <?php print $lang['administration']; ?>
                    </a>
                    <?php } ?>
                    <a href="<?php print $site_url; ?>user/administration">
                        <i class="fa fa-user"></i> <?php print $lang['account-data']; ?>
                    </a>
                    <a href="<?php print $site_url; ?>user/characters">
                        <i class="fa fa-users"></i> <?php print $lang['chars-list']; ?>
                    </a>
                    <?php if($shop_url && $shop_url != '#') { ?>
                    <a href="<?php print $shop_url; ?>" target="_blank" class="gold-premium-link">
                        <i class="fas fa-shopping-cart"></i> <?php print $lang['item-shop']; ?>
                    </a>
                    <?php } ?>
                    <a class="logout-link" href="<?php print $site_url; ?>users/logout">
                        <i class="fas fa-sign-out-alt"></i> <?php print $lang['logout']; ?>
                    </a>
                </div>
                <?php } ?>
            </aside>

        </div>
    </div>

    <!-- ====================================
         FOOTER
         ==================================== -->
    <footer class="footer-section">
        <div class="footer-content">
            <p>&copy; <?php echo date('Y'); ?> <a href="<?php echo $site_url; ?>"><?php print $site_title; ?></a> - All rights reserved.</p>
            <div class="footer-sponsor">
                <p>Sponsored by</p>
                <a href="https://www.inforge.net/" target="_blank" rel="noopener noreferrer">
                    <img src="<?php echo $site_url; ?>images/logo_inf.png" alt="Inforge" class="sponsor-logo">
                </a>
            </div>
        </div>
    </footer>
    
    <!-- ====================================
         SCRIPTS
         ==================================== -->
    <!-- jQuery from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.4/dist/jquery.min.js" integrity="sha256-oP6HI9z1XaZNBrJURtCoUT5SUnxFr8s3BzRl+cbzUq8=" crossorigin="anonymous"></script>

    <!-- Bootstrap 5 Bundle (includes Popper.js) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>

    <script>var site_url = "<?php print $site_url; ?>";</script>

    <?php if($page != 'admin') { ?>
    <!-- JavaScript del sito (esclusi dal pannello admin) -->
    <script src="<?php print $site_url; ?>js/app.js?v=<?php echo time(); ?>"></script>
    <script src="<?php print $site_url; ?>js/features.js?v=<?php echo time(); ?>"></script>
    <?php } ?>

    <?php if($is_homepage) { ?>
    <!-- Homepage Premium 2025 JavaScript - Solo Homepage -->
    <script src="<?php print $site_url; ?>js/homepage-premium.js?v=<?php echo time(); ?>"></script>
    <script src="<?php print $site_url; ?>js/wow-effects-premium.js?v=<?php echo time(); ?>"></script>
    <?php } ?>

    <?php include 'include/functions/footer.php'; ?>
</body>
</html>
<?php @ob_end_flush(); ?>