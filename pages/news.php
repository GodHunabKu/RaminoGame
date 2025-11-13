<style>
.news-page-modern {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

.news-hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 20px;
    padding: 40px;
    margin-bottom: 30px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
}

.news-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(231, 76, 60, 0.1) 0%, transparent 70%);
    animation: pulse 8s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 0.8; }
}

.news-hero-content {
    position: relative;
    z-index: 1;
}

.hero-icon {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    box-shadow: 0 8px 25px rgba(231, 76, 60, 0.4);
}

.hero-icon i {
    font-size: 35px;
    color: #fff;
}

.news-hero h1 {
    font-size: 2.5rem;
    font-weight: 700;
    text-align: center;
    margin: 0 0 15px 0;
    background: linear-gradient(135deg, #fff 0%, #E74C3C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.news-tabs {
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
}

.news-tab {
    padding: 12px 30px;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(231, 76, 60, 0.3);
    border-radius: 50px;
    color: #fff;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.news-tab::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(231, 76, 60, 0.3), transparent);
    transition: left 0.5s;
}

.news-tab:hover::before {
    left: 100%;
}

.news-tab:hover {
    background: rgba(231, 76, 60, 0.1);
    border-color: #E74C3C;
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(231, 76, 60, 0.3);
}

.news-tab.active {
    background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
    border-color: #E74C3C;
    box-shadow: 0 5px 20px rgba(231, 76, 60, 0.4);
}

.alert-modern {
    background: linear-gradient(135deg, rgba(220, 53, 69, 0.15) 0%, rgba(220, 53, 69, 0.05) 100%);
    border: 2px solid rgba(220, 53, 69, 0.5);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    color: #fff;
    display: flex;
    align-items: center;
    gap: 15px;
    box-shadow: 0 5px 20px rgba(220, 53, 69, 0.2);
}

.alert-modern i {
    font-size: 24px;
    color: #dc3545;
}

.alert-modern.server-offline {
    background: linear-gradient(135deg, rgba(255, 193, 7, 0.15) 0%, rgba(255, 193, 7, 0.05) 100%);
    border-color: rgba(255, 193, 7, 0.5);
    box-shadow: 0 5px 20px rgba(255, 193, 7, 0.2);
}

.alert-modern.server-offline i {
    color: #ffc107;
}

.news-layout {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 30px;
    align-items: start;
}

.news-main {
    min-height: 400px;
}

.discord-sidebar {
    position: sticky;
    top: 20px;
}

.discord-widget-container {
    background: linear-gradient(135deg, rgba(114, 137, 218, 0.1) 0%, rgba(114, 137, 218, 0.05) 100%);
    border: 2px solid rgba(114, 137, 218, 0.3);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.discord-widget-container::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(135deg, #7289DA, #5865F2, #7289DA);
    border-radius: 20px;
    z-index: -1;
    opacity: 0;
    transition: opacity 0.3s;
}

.discord-widget-container:hover::before {
    opacity: 0.3;
}

.discord-widget-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(114, 137, 218, 0.4);
}

.discord-widget-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid rgba(114, 137, 218, 0.3);
}

.discord-icon {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #7289DA 0%, #5865F2 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 5px 20px rgba(114, 137, 218, 0.4);
}

.discord-icon i {
    font-size: 25px;
    color: #fff;
}

.discord-widget-title {
    flex: 1;
}

.discord-widget-title h3 {
    margin: 0 0 5px 0;
    font-size: 1.3rem;
    font-weight: 700;
    color: #fff;
}

.discord-widget-title p {
    margin: 0;
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.6);
}

.discord-iframe-wrapper {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 20px rgba(0,0,0,0.3);
}

.discord-iframe-wrapper iframe {
    display: block;
    width: 100%;
    border: none;
    border-radius: 15px;
}

.pagination-wrapper {
    margin-top: 30px;
    display: flex;
    justify-content: center;
}

/* Responsive Design */
@media (max-width: 1024px) {
    .news-layout {
        grid-template-columns: 1fr;
    }

    .discord-sidebar {
        position: static;
        margin-top: 30px;
    }

    .discord-widget-container {
        max-width: 600px;
        margin: 0 auto;
    }
}

@media (max-width: 768px) {
    .news-hero {
        padding: 30px 20px;
    }

    .news-hero h1 {
        font-size: 1.8rem;
    }

    .news-tabs {
        gap: 10px;
    }

    .news-tab {
        padding: 10px 20px;
        font-size: 0.9rem;
    }

    .discord-widget-container {
        padding: 20px;
    }

    .discord-iframe-wrapper iframe {
        height: 400px;
    }
}

@media (max-width: 480px) {
    .news-page-modern {
        padding: 15px;
    }

    .news-hero {
        padding: 25px 15px;
    }

    .news-hero h1 {
        font-size: 1.5rem;
    }

    .hero-icon {
        width: 60px;
        height: 60px;
    }

    .hero-icon i {
        font-size: 28px;
    }

    .news-tab {
        padding: 8px 15px;
        font-size: 0.85rem;
    }

    .discord-iframe-wrapper iframe {
        height: 350px;
    }
}
</style>

<div class="news-page-modern">
    <!-- Hero Section -->
    <div class="news-hero">
        <div class="news-hero-content">
            <div class="hero-icon">
                <i class="fas fa-newspaper"></i>
            </div>
            <h1><?php print $lang['news']; ?></h1>
            <div class="news-tabs">
                <?php
                $cat = 0;
                if(isset($_GET['category']) && (int)$_GET['category']>0 && (int)$_GET['category']<=2)
                    $cat = $_GET['category'];

                $categories = array(
                    0 => "All news",
                    1 => "Updates",
                    2 => "Events"
                );

                foreach($categories as $key => $value) {
                    $activeClass = ($key == $cat) ? 'active' : '';
                    print '<a href="'.$site_url.'news/'.$key.'/1" class="news-tab '.$activeClass.'">';
                    if($key == 0) print '<i class="fas fa-list"></i> ';
                    elseif($key == 1) print '<i class="fas fa-sync-alt"></i> ';
                    elseif($key == 2) print '<i class="fas fa-calendar-star"></i> ';
                    print $value.'</a>';
                }
                ?>
            </div>
        </div>
    </div>

    <!-- Alerts -->
    <?php if($offline): ?>
    <div class="alert-modern server-offline">
        <i class="fas fa-exclamation-triangle"></i>
        <strong><?php print $lang['server-offline']; ?></strong>
    </div>
    <?php endif; ?>

    <?php if (version_compare($php_version = phpversion(), '5.6.0', '<')): ?>
    <div class="alert-modern">
        <i class="fas fa-exclamation-circle"></i>
        <span>Metin2CMS works with a PHP version >= 5.6.0. At this time, the server is running version <?php print $php_version; ?>.</span>
    </div>
    <?php endif; ?>

    <!-- Main Content Layout -->
    <div class="news-layout">
        <!-- News Content -->
        <div class="news-main">
            <?php
            // Admin add news form
            if(!$offline && $database->is_loggedin()) {
                if($web_admin >= $jsondataPrivileges['news']) {
                    include 'include/functions/add-news.php';
                }
            }

            // News display
            $query = "SELECT * FROM news ORDER BY id DESC";
            if($cat) {
                $query = "SELECT * FROM news WHERE category = ".$cat." ORDER BY id DESC";
            }
            $records_per_page = intval(getJsonSettings("news"));

            $newquery = $paginate->paging($query, $records_per_page);
            $paginate->dataview($newquery, $lang['sure?'], $web_admin, $jsondataPrivileges['news'], $site_url, $lang['read-more']);
            ?>

            <div class="pagination-wrapper">
                <?php
                $paginate->paginglink($query, $records_per_page, $lang['first-page'], $lang['last-page'], $site_url, $cat);
                ?>
            </div>
        </div>

        <!-- Discord Widget Sidebar -->
        <div class="discord-sidebar">
            <div class="discord-widget-container">
                <div class="discord-widget-header">
                    <div class="discord-icon">
                        <i class="fab fa-discord"></i>
                    </div>
                    <div class="discord-widget-title">
                        <h3>Join Our Discord</h3>
                        <p>Chat with the community</p>
                    </div>
                </div>
                <div class="discord-iframe-wrapper">
                    <iframe
                        src="https://discord.com/widget?id=824954226114560001&theme=dark"
                        width="350"
                        height="500"
                        allowtransparency="true"
                        frameborder="0"
                        sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts">
                    </iframe>
                </div>
            </div>
        </div>
    </div>
</div>
